"""
CropGuard Farmer Diagnostic Portal
Leaf photo upload & camera input, crop selection, Open-Meteo live weather risk scoring,
Hugging Face image classification with top-3 predictions and 60% confidence threshold safeguard,
trilingual Integrated Pest Management (IPM) advisory, and SQLite persistence.
"""

import os
import json
from PIL import Image
import streamlit as st

import db
import model
import weather

# Page Config
st.set_page_config(
    page_title="Farmer Diagnostic Portal | CropGuard",
    page_icon="🌾",
    layout="wide",
)

# Custom styles
st.markdown(
    """
    <style>
    .portal-banner {
        background: linear-gradient(90deg, #134e5e 0%, #71b280 100%);
        padding: 18px 24px;
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
    .uncertain-alert {
        background-color: #fff1f2;
        border: 2px solid #fda4af;
        border-left: 8px solid #e11d48;
        padding: 20px;
        border-radius: 10px;
        margin: 16px 0;
    }
    .diagnosis-success {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 6px solid #16a34a;
        padding: 18px;
        border-radius: 10px;
        margin: 16px 0;
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
        padding: 12px 16px;
        border-radius: 6px;
        color: #854d0e;
        font-size: 0.85rem;
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

# Header Banner
st.markdown(
    """
    <div class="portal-banner">
        <h2>🌾 Farmer Disease Diagnostic & IPM Advisory Portal</h2>
        <p style="margin: 4px 0 0 0; opacity: 0.95;">Early symptom classification, local weather epidemiology, and actionable non-chemical crop defense</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Top Bar: Language & Crop Selector
col_top1, col_top2, col_top3 = st.columns([1.5, 1.5, 2])

with col_top1:
    language_choice = st.selectbox(
        "🌐 Choose Language / भाषा / भाषा निवडा",
        options=["English", "हिन्दी (Hindi)", "मराठी (Marathi)"],
        index=0,
    )
    lang_code = "en"
    if "हिन्दी" in language_choice:
        lang_code = "hi"
    elif "मराठी" in language_choice:
        lang_code = "mr"

with col_top2:
    crop_selected = st.selectbox(
        "🌱 Select Target Crop",
        options=["Tomato", "Cotton", "Onion"],
        index=0,
    )

with col_top3:
    # Location selection
    locations_preset = {
        "Pune (Default)": (18.5204, 73.8567),
        "Nashik (Niphad / Kalwan)": (20.0768, 74.1089),
        "Jalgaon (Khandesh Cotton)": (21.0077, 75.5626),
        "Ahmednagar (Rahuri / Sangamner)": (19.3942, 74.6514),
        "Solapur (Pandharpur)": (17.6775, 75.3214),
        "Nagpur (Vidarbha Belt)": (21.1458, 79.0882),
        "Kolhapur (Shirol)": (16.7381, 74.5936),
        "Chhatrapati Sambhaji Nagar": (19.8762, 75.3433),
        "Custom Coordinates": (0.0, 0.0),
    }
    loc_preset_choice = st.selectbox("📍 Select Field Location", options=list(locations_preset.keys()), index=0)

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

# Two-column layout: Left for Image & Model, Right for Weather Risk & Advisory
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("📸 Step 1: Provide Leaf Photo")
    input_method = st.radio(
        "Choose image input source:",
        options=["📁 Upload File", "📷 Use Camera Input", "🧪 Instant Test Demo Samples"],
        horizontal=True,
    )

    image_to_process = None
    image_name = "farmer_photo.jpg"

    if input_method == "📁 Upload File":
        uploaded_file = st.file_uploader(
            "Upload clear leaf photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            help="Take photo in good natural lighting against neutral background",
        )
        if uploaded_file is not None:
            image_to_process = Image.open(uploaded_file)
            image_name = uploaded_file.name
            st.image(image_to_process, caption=f"Uploaded: {image_name}", use_container_width=True)

    elif input_method == "📷 Use Camera Input":
        camera_img = st.camera_input("Capture live photo of affected leaf")
        if camera_img is not None:
            image_to_process = Image.open(camera_img)
            image_name = "camera_capture.jpg"
            st.image(image_to_process, caption="Live Camera Photo", use_container_width=True)

    else:
        st.info("Select a pre-configured sample to test the AI model and edge cases instantly:")
        sample_choice = st.selectbox(
            "Select Sample Case:",
            options=[
                "Tomato - Early Blight (Target Rings)",
                "Tomato - Late Blight (Rotting Water Lesions)",
                "Tomato - Healthy Leaf (Control)",
                "Cotton - Bacterial Blight (Angular Spots)",
                "Onion - Purple Blotch (Spindle Lesion)",
                "Uncertain Sample (Low Confidence < 60% Demo)",
            ],
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
            st.image(image_to_process, caption=f"Selected Sample: {sample_choice}", use_container_width=True)
        else:
            # Create inline dummy fallback
            image_to_process = Image.new("RGB", (300, 300), (50, 140, 50))
            image_name = "sample_fallback.jpg"
            st.image(image_to_process, caption="Demo Leaf Canvas", use_container_width=True)

    # Diagnostic trigger button
    btn_analyze = st.button("🔍 Run Disease Diagnosis", type="primary", use_container_width=True)

with col_right:
    st.subheader(f"🌦️ Step 2: Live Weather Epidemiology ({location_label})")
    with st.spinner("Fetching real-time atmospheric data from Open-Meteo..."):
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
        st.metric("🌡️ Temp", f"{weather_info['temperature']}°C")
    with wk2:
        st.metric("💧 Humidity", f"{weather_info['humidity']}%")
    with wk3:
        st.metric("🌧️ Rainfall", f"{weather_info['precipitation']} mm")
    with wk4:
        st.metric("💨 Wind", f"{weather_info['wind_speed']} km/h")

    # Risk badge
    if risk_level == "High":
        st.markdown(
            f'<div class="risk-high">⚠️ FUNGAL / PEST OUTBREAK RISK: HIGH<br><span style="font-weight: 400; font-size: 0.9rem;">{risk_expl}</span></div>',
            unsafe_allow_html=True,
        )
    elif risk_level == "Medium":
        st.markdown(
            f'<div class="risk-medium">⚡ FUNGAL / PEST OUTBREAK RISK: MEDIUM<br><span style="font-weight: 400; font-size: 0.9rem;">{risk_expl}</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="risk-low">✅ FUNGAL / PEST OUTBREAK RISK: LOW<br><span style="font-weight: 400; font-size: 0.9rem;">{risk_expl}</span></div>',
            unsafe_allow_html=True,
        )

    if not weather_info["success"]:
        st.caption(f"ℹ️ {weather_info['error']}")

# Bottom section: Diagnostic Output & IPM Advisory
st.divider()

if btn_analyze or (image_to_process is not None and "last_analyzed_img" in st.session_state and st.session_state["last_analyzed_img"] == image_name):
    st.session_state["last_analyzed_img"] = image_name

    with st.spinner("Classifying plant disease using Hugging Face vision model..."):
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

    st.subheader("🎯 Step 3: Diagnostic Results")

    # Display Top-3 Predictions Bar
    st.markdown("##### 📊 Top-3 Candidate Predictions (Confidence Breakdown):")
    for idx, pred in enumerate(predictions):
        p_col1, p_col2 = st.columns([3, 1])
        with p_col1:
            st.write(f"**{idx + 1}. {pred['display_name']}**")
            st.progress(float(pred["confidence"]))
        with p_col2:
            st.metric(label="Probability", value=pred["confidence_pct"])

    st.caption(f"🤖 Model Backbone: {res['model_source']} | Registered Report ID: #{report_id}")
    if res.get("notice"):
        st.caption(f"ℹ️ {res['notice']}")

    st.markdown("---")

    # Strict Requirement: If top confidence < 60%, show "Uncertain – please consult an agriculture officer" instead of a diagnosis
    if is_uncertain:
        st.markdown(
            f"""
            <div class="uncertain-alert">
                <h3 style="color: #b91c1c; margin-top: 0;">⚠️ Uncertain – please consult an agriculture officer</h3>
                <p style="font-size: 1.05rem; margin-bottom: 8px;">
                    <strong>Top confidence score is {top_conf*100:.1f}% (below the required 60.0% threshold).</strong>
                </p>
                <p>To prevent erroneous diagnoses or inappropriate chemical expenditures, CropGuard has flagged this case for human expert verification.</p>
                <ul>
                    <li>This case has been automatically logged in the <strong>Officer Surveillance Dashboard (Report #{report_id})</strong> for review by your Taluka/District Agriculture Officer.</li>
                    <li><strong>Tips for better photos:</strong> Retake photo in bright natural daytime light, focus sharply on active lesion margins, ensure the leaf is flat, and wipe any camera lens smudge.</li>
                    <li>Visit your nearest <strong>Krishi Vigyan Kendra (KVK)</strong> or consult the local Agriculture Extension Officer with a fresh leaf sample in a sealed plastic bag.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Confident Diagnosis (>= 60%)
        disease_info = advisory_db.get("diseases", {}).get(top_disease, {})
        lang_data = disease_info.get(lang_code, disease_info.get("en", {}))

        disease_name = lang_data.get("name", res["top_display_name"])
        scientific_name = disease_info.get("scientific_name", "")
        pathogen = lang_data.get("pathogen", "Pathogen")
        symptoms = lang_data.get("symptoms", "")

        st.markdown(
            f"""
            <div class="diagnosis-success">
                <span style="background-color: #16a34a; color: white; padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 0.8rem;">CONFIRMED DIAGNOSIS ({top_conf*100:.1f}%)</span>
                <h2 style="color: #14532d; margin: 8px 0 4px 0;">{disease_name}</h2>
                <p style="color: #166534; font-size: 1rem; margin-bottom: 8px;"><strong>Scientific Name / Pathogen:</strong> <em>{scientific_name}</em> | {pathogen}</p>
                <p style="color: #1f2937; margin: 0;"><strong>Symptoms:</strong> {symptoms}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### 📋 Integrated Pest Management (IPM) Advisory")
        st.markdown(
            f"*Language Selected: **{language_choice}** | Following ICAR & Central Institute Guidelines*"
        )

        tab_cult, tab_bio, tab_chem, tab_safe = st.tabs([
            "🌱 Cultural Practices",
            "🧫 Biological Controls",
            "🧪 Chemical (Last Resort)",
            "🦺 Safety & Pre-Harvest",
        ])

        with tab_cult:
            st.markdown("#### Cultural & Agronomic Interventions:")
            for item in lang_data.get("cultural", []):
                st.markdown(f"- {item}")

        with tab_bio:
            st.markdown("#### Biological & Organic Biocontrols:")
            for item in lang_data.get("biological", []):
                st.markdown(f"- {item}")

        with tab_chem:
            st.markdown("#### Chemical Controls (Strictly As Last Resort):")
            st.warning("⚠️ Strictly follow Economic Threshold Levels (ETL). Never apply calendar prophylactic chemical sprays.")
            for item in lang_data.get("chemical_last", []):
                st.markdown(f"- {item}")

        with tab_safe:
            st.markdown("#### Protective Equipment & Health Measures:")
            for item in lang_data.get("safety_notes", []):
                st.markdown(f"- {item}")

        # Official Disclaimer in current language
        disclaimer_text = advisory_db.get("disclaimer", {}).get(lang_code, advisory_db.get("disclaimer", {}).get("en", ""))
        st.markdown(
            f"""
            <div class="disclaimer-banner">
                <strong>📜 Regulatory Notice:</strong> {disclaimer_text}
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.info("👆 Provide or select an image on the left and click **'Run Disease Diagnosis'** to classify symptoms.")
