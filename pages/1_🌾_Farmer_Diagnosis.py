"""
CropGuard Farmer Diagnostic Portal
Leaf photo upload & camera input, crop selection, Open-Meteo live weather risk scoring,
Hugging Face / Computer-Vision symptom engine with top-3 predictions,
calibrated confidence calculations, trilingual Integrated Pest Management (IPM) advisory,
and SQLite persistence.
Fully localized across English, Hindi, and Marathi with persistent session state.
"""

import os
import json
from PIL import Image
import streamlit as st

import db
import model
import weather
import translations
from translations import t

# Page Config
st.set_page_config(
    page_title="Farmer Diagnostic Portal | CropGuard",
    page_icon="logo.jpeg",
    layout="wide",
)

# Initialize language session state
translations.init_language_state()
lang_code = translations.get_current_language()

# Custom styles
st.markdown(
    """
    <style>
    .portal-banner {
        background: linear-gradient(90deg, #134e5e 0%, #71b280 100%);
        padding: 20px 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
    .portal-banner h2 {
        color: white !important;
        margin: 0;
        font-size: 1.8rem;
    }
    .risk-high {
        background-color: #fee2e2;
        border-left: 5px solid #ef4444;
        color: #991b1b;
        padding: 12px 16px;
        border-radius: 6px;
        font-weight: 600;
    }
    .risk-medium {
        background-color: #fef3c7;
        border-left: 5px solid #f59e0b;
        color: #92400e;
        padding: 12px 16px;
        border-radius: 6px;
        font-weight: 600;
    }
    .risk-low {
        background-color: #dcfce7;
        border-left: 5px solid #10b981;
        color: #065f46;
        padding: 12px 16px;
        border-radius: 6px;
        font-weight: 600;
    }
    .ipm-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .disclaimer-banner {
        background-color: #fefce8;
        border: 1px solid #fef08a;
        border-left: 4px solid #ca8a04;
        padding: 14px 18px;
        border-radius: 6px;
        color: #854d0e;
        font-size: 0.88rem;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load advisory.json
@st.cache_data
def load_advisory_data():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "advisory.json")
    if not os.path.exists(path):
        path = "advisory.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

advisory_db = load_advisory_data()

# Clean Organized Navigation Sidebar
with st.sidebar:
    st.image("logo.jpeg", use_container_width=True)
    
    # Persistent Language Selector
    lang_code = translations.render_language_selector(sidebar=True, key_prefix="farmer")

    st.markdown(f"### 📍 {t('nav_heading', lang_code)}")
    st.page_link("app.py", label=t("nav_home", lang_code), icon="🏠")
    st.page_link("pages/1_🌾_Farmer_Diagnosis.py", label=t("nav_farmer", lang_code), icon="🌾")
    st.page_link("pages/2_🛡️_Officer_Dashboard.py", label=t("nav_officer", lang_code), icon="🛡️")
    st.page_link("pages/3_📚_Disease_Advisory.py", label=t("nav_advisory", lang_code), icon="📚")
    st.divider()
    
    st.markdown(f"### ⚙️ {t('system_status', lang_code)}")
    engine_status = model.get_model_engine_status()
    st.caption(f"{engine_status['status_badge']}\n\n*{engine_status['engine_name']}*")
    st.divider()
    st.caption(t("footer_credit", lang_code))

# Header Banner
st.markdown(
    f"""
    <div class="portal-banner">
        <h2>{t('portal_banner_title', lang_code)}</h2>
        <p style="margin: 4px 0 0 0; opacity: 0.95;">{t('portal_banner_subtitle', lang_code)}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Top Bar: Crop and Location Selectors
col_top1, col_top2 = st.columns([1, 1])

crop_options = ["Tomato", "Cotton", "Onion"]
crop_display_map = {
    "Tomato": {"en": "🍅 Tomato", "hi": "🍅 टमाटर (Tomato)", "mr": "🍅 टोमॅटो (Tomato)"},
    "Cotton": {"en": "🌿 Cotton", "hi": "🌿 कपास (Cotton)", "mr": "🌿 कापूस (Cotton)"},
    "Onion": {"en": "🧅 Onion", "hi": "🧅 प्याज (Onion)", "mr": "🧅 कांदा (Onion)"},
}

with col_top1:
    crop_selected = st.selectbox(
        t("select_crop_label", lang_code),
        options=crop_options,
        format_func=lambda x: crop_display_map.get(x, {}).get(lang_code, x),
        index=0,
    )

with col_top2:
    locations_preset = {
        "Pune (Western Maharashtra)": (18.5204, 73.8567),
        "Nashik (Niphad / Kalwan Onion Belt)": (20.0768, 74.1089),
        "Jalgaon (Khandesh Cotton Belt)": (21.0077, 75.5626),
        "Ahmednagar (Rahuri / Sangamner)": (19.3942, 74.6514),
        "Solapur (Pandharpur / Barshi)": (17.6775, 75.3214),
        "Nagpur (Vidarbha Cotton Belt)": (21.1458, 79.0882),
        "Kolhapur (Shirol / Hatkanangle)": (16.7381, 74.5936),
        "Chhatrapati Sambhaji Nagar": (19.8762, 75.3433),
        "Custom Coordinates": (0.0, 0.0),
    }
    loc_preset_choice = st.selectbox(
        t("select_location_label", lang_code),
        options=list(locations_preset.keys()),
        index=0,
    )

if loc_preset_choice == "Custom Coordinates":
    col_lat, col_lon = st.columns(2)
    with col_lat:
        user_lat = st.number_input("Latitude", value=18.5204, format="%.4f")
    with col_lon:
        user_lon = st.number_input("Longitude", value=73.8567, format="%.4f")
    location_label = f"Custom ({user_lat:.2f}, {user_lon:.2f})"
else:
    user_lat, user_lon = locations_preset[loc_preset_choice]
    location_label = loc_preset_choice

st.divider()

# Two-column layout: Left for Image & Model, Right for Weather Risk & Epidemiology
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader(t("step1_heading", lang_code))
    input_method_choices = [
        t("input_upload", lang_code),
        t("input_camera", lang_code),
        t("input_samples", lang_code),
    ]
    input_method = st.radio(
        t("input_method_label", lang_code),
        options=input_method_choices,
        horizontal=True,
    )

    image_to_process = None
    image_name = "farmer_photo.jpg"

    if input_method == t("input_upload", lang_code):
        uploaded_file = st.file_uploader(
            t("upload_instruction", lang_code),
            type=["jpg", "jpeg", "png"],
            help=t("upload_help", lang_code),
        )
        if uploaded_file is not None:
            image_to_process = Image.open(uploaded_file)
            image_name = uploaded_file.name
            st.image(image_to_process, caption=f"Uploaded: {image_name}", use_container_width=True)

    elif input_method == t("input_camera", lang_code):
        camera_img = st.camera_input(t("camera_instruction", lang_code))
        if camera_img is not None:
            image_to_process = Image.open(camera_img)
            image_name = "camera_capture.jpg"
            st.image(image_to_process, caption="Live Camera Photo", use_container_width=True)

    else:
        st.info(t("sample_helper_text", lang_code))
        sample_options = [
            "Tomato - Early Blight (Target Rings)",
            "Tomato - Late Blight (Rotting Water Lesions)",
            "Tomato - Healthy Leaf (Control)",
            "Cotton - Bacterial Blight (Angular Spots)",
            "Onion - Purple Blotch (Spindle Lesion)",
            "Uncertain Sample (Low Confidence < 60% Demo)",
        ]
        sample_choice = st.selectbox(
            t("sample_instruction", lang_code),
            options=sample_options,
        )

        sample_mapping = {
            "Tomato - Early Blight (Target Rings)": ("tomato_early_blight_sample.jpg", "Tomato"),
            "Tomato - Late Blight (Rotting Water Lesions)": ("tomato_late_blight_sample.jpg", "Tomato"),
            "Tomato - Healthy Leaf (Control)": ("tomato_healthy_sample.jpg", "Tomato"),
            "Cotton - Bacterial Blight (Angular Spots)": ("cotton_bacterial_blight_sample.jpg", "Cotton"),
            "Onion - Purple Blotch (Spindle Lesion)": ("onion_purple_blotch_sample.jpg", "Onion"),
            "Uncertain Sample (Low Confidence < 60% Demo)": ("uncertain_sample.jpg", crop_selected),
        }

        sample_file, auto_crop = sample_mapping[sample_choice]
        sample_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "samples", sample_file)

        # Generate on the fly if not exists
        if not os.path.exists(sample_path):
            try:
                import generate_samples
                generate_samples.generate_all_samples()
            except Exception:
                pass

        if os.path.exists(sample_path):
            image_to_process = Image.open(sample_path)
            image_name = sample_file
            st.image(image_to_process, caption=f"Sample: {sample_choice}", use_container_width=True)
        else:
            image_to_process = Image.new("RGB", (300, 300), (50, 140, 50))
            image_name = "sample_fallback.jpg"
            st.image(image_to_process, caption="Demo Leaf Canvas", use_container_width=True)

    btn_analyze = st.button(t("btn_run_diagnosis", lang_code), type="primary", use_container_width=True)

with col_right:
    st.subheader(f"{t('step2_heading', lang_code)} ({location_label})")
    with st.spinner(t("weather_fetching", lang_code)):
        weather_info = weather.get_current_weather(user_lat, user_lon)
        risk_level, risk_expl, risk_metrics = weather.compute_disease_weather_risk(
            weather_info["temperature"],
            weather_info["humidity"],
            weather_info["precipitation"],
            crop_selected.lower(),
        )

    # Weather KPI cards
    wk1, wk2, wk3, wk4 = st.columns(4)
    with wk1:
        st.metric(t("weather_temp", lang_code), f"{weather_info['temperature']}°C")
    with wk2:
        st.metric(t("weather_humidity", lang_code), f"{weather_info['humidity']}%")
    with wk3:
        st.metric(t("weather_rain", lang_code), f"{weather_info['precipitation']} mm")
    with wk4:
        st.metric(t("weather_wind", lang_code), f"{weather_info['wind_speed']} km/h")

    # Risk badge
    if risk_level == "High":
        st.markdown(
            f'<div class="risk-high">{t("risk_high_badge", lang_code)}<br><span style="font-weight: 400; font-size: 0.9rem;">{risk_expl}</span></div>',
            unsafe_allow_html=True,
        )
    elif risk_level == "Medium":
        st.markdown(
            f'<div class="risk-medium">{t("risk_med_badge", lang_code)}<br><span style="font-weight: 400; font-size: 0.9rem;">{risk_expl}</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="risk-low">{t("risk_low_badge", lang_code)}<br><span style="font-weight: 400; font-size: 0.9rem;">{risk_expl}</span></div>',
            unsafe_allow_html=True,
        )

    if not weather_info["success"]:
        st.caption(f"ℹ️ {weather_info['error']}")

# Bottom section: Diagnostic Output & IPM Advisory
st.divider()

if btn_analyze or (image_to_process is not None and "last_analyzed_img" in st.session_state and st.session_state["last_analyzed_img"] == image_name):
    st.session_state["last_analyzed_img"] = image_name

    with st.spinner("Analyzing plant foliage features and disease symptoms..."):
        res = model.classify_crop_image(image_to_process, crop_selected.lower())

    top_disease = res["top_disease"]
    top_conf = res["top_confidence"]
    is_uncertain = res["is_uncertain"]
    predictions = res["top_predictions"]

    # Save to SQLite
    report_id = db.save_report(
        crop=crop_selected.lower(),
        predicted_disease=top_disease,
        confidence=top_conf,
        latitude=user_lat,
        longitude=user_lon,
        location_name=location_label,
        language=lang_code,
        is_uncertain=is_uncertain,
        temperature=weather_info["temperature"],
        humidity=weather_info["humidity"],
        rainfall=weather_info["precipitation"],
        weather_risk=risk_level,
        image_name=image_name,
    )

    st.subheader(t("step3_heading", lang_code))

    # Preliminary Screening Notice explaining predictions are statistical screening estimates
    st.info(t("screening_notice", lang_code))

    # Display Top Candidate Predictions with Confidence Breakdown
    st.markdown(f"##### {t('candidate_breakdown_title', lang_code)}")
    for idx, pred in enumerate(predictions):
        p_col1, p_col2 = st.columns([3, 1])
        d_localized = translations.get_disease_name(pred["disease_id"], lang_code)
        with p_col1:
            st.write(f"**{idx + 1}. {d_localized}**")
            st.progress(float(pred["confidence"]))
        with p_col2:
            st.metric(label=t("match_confidence_lbl", lang_code), value=pred["confidence_pct"])

    st.caption(f"🤖 Vision Backbone: {res['model_source']} | Stored Surveillance Record: #{report_id}")
    if res.get("notice"):
        st.caption(f"ℹ️ {res['notice']}")

    st.markdown("---")

    # Fetch disease knowledge from advisory_db
    disease_info = advisory_db.get("diseases", {}).get(top_disease, {})
    lang_data = disease_info.get(lang_code, disease_info.get("en", {}))
    disease_name_localized = translations.get_disease_name(top_disease, lang_code)
    scientific_name = disease_info.get("scientific_name", "Pathogen")
    pathogen = lang_data.get("pathogen", "Plant Pathogen")
    symptoms = lang_data.get("symptoms", "Foliar discoloration and tissue lesions.")

    # High vs Low Confidence / Inconclusive Presentation
    if is_uncertain:
        # Actionable Low Confidence Guidance
        st.markdown(
            f"""
            <div style="background-color: #fffbeb; border: 2px solid #fde68a; border-left: 6px solid #d97706; padding: 20px; border-radius: 12px; margin-bottom: 24px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="font-size: 1.3rem;">⚠️</span>
                    <h3 style="color: #92400e; margin: 0; font-size: 1.25rem; font-weight: 800;">
                        {t('low_conf_heading', lang_code)} ({top_conf*100:.1f}%)
                    </h3>
                </div>
                <p style="color: #78350f; font-size: 0.95rem; line-height: 1.5; margin-bottom: 12px;">
                    {t('low_conf_expl', lang_code).format(disease=disease_name_localized, conf=f"{top_conf*100:.1f}%")}
                </p>
                <div style="background-color: #ffffff; border: 1px solid #fef3c7; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                    <strong style="color: #92400e; font-size: 0.9rem;">{t('photo_guide_title', lang_code)}</strong>
                    <ul style="color: #451a03; font-size: 0.88rem; margin: 6px 0 0 0; padding-left: 20px;">
                        <li>{t('photo_guide_1', lang_code)}</li>
                        <li>{t('photo_guide_2', lang_code)}</li>
                        <li>{t('photo_guide_3', lang_code)}</li>
                        <li>{t('photo_guide_4', lang_code)}</li>
                    </ul>
                </div>
                <p style="color: #92400e; font-size: 0.85rem; margin: 0;">
                    ✓ <em>Logged for agricultural officer review as Surveillance Record #{report_id}.</em>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # High Confidence Visual Match (>= 60%)
        st.markdown(
            f"""
            <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-left: 6px solid #16a34a; padding: 20px; border-radius: 12px; margin-bottom: 24px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                    <span style="background-color: #16a34a; color: white; padding: 3px 10px; border-radius: 9999px; font-weight: 700; font-size: 0.75rem; text-transform: uppercase;">
                        {t('candidate_match_badge', lang_code)} ({top_conf*100:.1f}%)
                    </span>
                    <span style="font-size: 0.8rem; color: #15803d; font-weight: 600;">Report #{report_id}</span>
                </div>
                <h2 style="color: #064e3b; margin: 4px 0 6px 0; font-size: 1.6rem; font-weight: 800;">{disease_name_localized}</h2>
                <p style="color: #047857; font-size: 0.95rem; margin-bottom: 8px;">
                    <strong>Pathogen:</strong> {pathogen} &nbsp;|&nbsp; <em>{scientific_name}</em>
                </p>
                <p style="color: #1e293b; font-size: 0.9rem; margin: 0; line-height: 1.5;">
                    <strong>Symptom Profile:</strong> {symptoms}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 5 STRUCTURED ACTIONABLE SECTIONS FOR THE FARMER
    st.markdown(f"### 📋 {t('protocol_heading', lang_code)}")
    st.caption(t("protocol_caption", lang_code))

    # Section A: Possible Disease & Observed Symptoms
    with st.expander(t("sec_a_title", lang_code), expanded=True):
        st.markdown(
            f"""
            - **{t('possible_diagnosis_label', lang_code)}:** **{disease_name_localized}**
            - **Scientific Name / Group:** *{scientific_name}* ({pathogen})
            - **Target Crop:** {crop_selected}
            - **Observed Field Symptoms:** {symptoms}
            - **Micro-Climate Epidemiological Risk:** Currently rated **{risk_level}** at {location_label} ({weather_info['temperature']}°C, {weather_info['humidity']}% Relative Humidity, {weather_info['precipitation']} mm rain).
            - **Diagnostic Notice:** Surface visual signs provide an automated screening estimate. Final confirmation through field scouting and expert consultation is always recommended.
            """
        )

    # Section B: Immediate Steps the Farmer Can Take
    with st.expander(t("sec_b_title", lang_code), expanded=True):
        st.markdown(
            f"""
            - {t('sec_b_1', lang_code)}
            - {t('sec_b_2', lang_code)}
            - {t('sec_b_3', lang_code)}
            - {t('sec_b_4', lang_code)}
            - {t('sec_b_5', lang_code)}
            """
        )

    # Section C: Disease-Specific Prevention Methods
    with st.expander(t("sec_c_title", lang_code), expanded=True):
        st.markdown(f"#### Prevention & Cultural Practices for {crop_selected} ({disease_name_localized}):")
        cultural_points = lang_data.get("cultural", [])
        if cultural_points:
            for pt in cultural_points:
                st.markdown(f"- {pt}")
        else:
            st.markdown(
                """
                - Practice crop rotation with non-host botanical families (cereals or pulses).
                - Plant certified pathogen-free seeds from reputable certified nurseries.
                - Utilize resistant or tolerant crop hybrids recommended by State Agricultural Universities.
                - Apply reflective organic mulches to reduce soil splash and insect landing.
                """
            )

    # Section D: Crop Hygiene, Watering, Drainage & Monitoring Recommendations
    with st.expander(t("sec_d_title", lang_code), expanded=True):
        st.markdown(
            f"""
            - **{t('sec_d_watering', lang_code)}**
            - **{t('sec_d_drainage', lang_code)}**
            - **{t('sec_d_spacing', lang_code)}**
            - **{t('sec_d_weeding', lang_code)}**
            - **{t('sec_d_monitoring', lang_code)}**
            """
        )

    # Section E: When to Seek Agricultural Expert Confirmation
    with st.expander(t("sec_e_title", lang_code), expanded=True):
        st.markdown(
            f"""
            **{t('sec_e_triggers_title', lang_code)}**
            - {t('sec_e_1', lang_code)}
            - {t('sec_e_2', lang_code)}
            - {t('sec_e_3', lang_code)}
            - {t('sec_e_4', lang_code)}
            
            **{t('sec_e_sample_guide', lang_code)}**
            """
        )

    # Monitored Treatments & Responsible Safeguards
    st.markdown("### 🧪 Monitored Treatments & Responsible Safeguards")
    tab_bio, tab_chem, tab_safe = st.tabs([
        t("tab_bio", lang_code),
        t("tab_chem", lang_code),
        t("tab_safe", lang_code),
    ])

    with tab_bio:
        st.markdown("#### Biological Controls & Bio-Pesticides:")
        bio_items = lang_data.get("biological", [])
        if bio_items:
            for item in bio_items:
                st.markdown(f"- {item}")
        else:
            st.markdown("- Apply *Trichoderma viride* or *Pseudomonas fluorescens* formulations during early morning or evening.")
            st.markdown("- Utilize 5% Neem Seed Kernel Extract (NSKE) as an organic deterrent against fungal sporulation and insect vectors.")

    with tab_chem:
        st.markdown("#### Chemical Controls (Strictly As Monitored Last Resort):")
        st.error(t("chem_warning", lang_code))
        chem_items = lang_data.get("chemical_last", [])
        for item in chem_items:
            st.markdown(f"- {item}")

    with tab_safe:
        st.markdown("#### Operator Health, PPE & Pre-Harvest Intervals:")
        safe_items = lang_data.get("safety_notes", [])
        for item in safe_items:
            st.markdown(f"- {item}")
        st.markdown(f"- **{t('phi_note', lang_code)}**")

    # Regulatory Notice
    disclaimer_text = advisory_db.get("disclaimer", {}).get(lang_code, advisory_db.get("disclaimer", {}).get("en", ""))
    st.markdown(
        f"""
        <div class="disclaimer-banner">
            <strong>📜 Official Agricultural Extension Advisory Notice:</strong><br>
            {disclaimer_text}
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    st.info("👆 Provide or select an image on the left and click **'Run Disease Diagnosis'** to classify symptoms.")
