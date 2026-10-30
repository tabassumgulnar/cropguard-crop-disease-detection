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
    page_icon="logo.jpeg",
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

# Clean Organized Navigation Sidebar
with st.sidebar:
    st.image("logo.jpeg", use_container_width=True)
    st.markdown("### 📍 Navigation")
    st.page_link("app.py", label="Home Dashboard", icon="🏠")
    st.page_link("pages/1_🌾_Farmer_Diagnosis.py", label="Farmer Diagnostic Portal", icon="🌾")
    st.page_link("pages/2_🛡️_Officer_Dashboard.py", label="Officer GIS Dashboard", icon="🛡️")
    st.page_link("pages/3_📚_Disease_Advisory.py", label="Trilingual IPM Catalog", icon="📚")
    st.divider()
    st.markdown("### ⚙️ Engine State")
    engine_status = model.get_model_engine_status()
    st.caption(f"{engine_status['status_badge']}\n\n*{engine_status['engine_name']}*")
    st.divider()
    st.caption("CropGuard • Open-Source Agro-Informatics")

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

    st.subheader("🎯 Step 3: Diagnostic Screening Results")

    # Clear explanation that predictions are statistical screening estimates, not confirmed lab diagnoses
    st.info(
        "ℹ️ **Preliminary Screening Notice:** AI visual predictions are automated screening estimates based on surface foliar symptoms. "
        "They are designed to support early scouting and do **not** replace laboratory pathogen isolation, culturing, or molecular tests. "
        "Always evaluate plant symptoms alongside field history, soil condition, and local weather."
    )

    # Display Top Candidate Predictions with Confidence Breakdown
    st.markdown("##### 📊 Top Candidate Disease Predictions (Probability Breakdown):")
    for idx, pred in enumerate(predictions):
        p_col1, p_col2 = st.columns([3, 1])
        with p_col1:
            st.write(f"**{idx + 1}. {pred['display_name']}**")
            st.progress(float(pred["confidence"]))
        with p_col2:
            st.metric(label="Match Confidence", value=pred["confidence_pct"])

    st.caption(f"🤖 Vision Backbone: {res['model_source']} | Stored Surveillance Record: #{report_id}")
    if res.get("notice"):
        st.caption(f"ℹ️ {res['notice']}")

    st.markdown("---")

    # Fetch disease knowledge from advisory_db
    disease_info = advisory_db.get("diseases", {}).get(top_disease, {})
    lang_data = disease_info.get(lang_code, disease_info.get("en", {}))
    disease_name = lang_data.get("name", res["top_display_name"])
    scientific_name = disease_info.get("scientific_name", "Pathogen")
    pathogen = lang_data.get("pathogen", "Plant Pathogen")
    symptoms = lang_data.get("symptoms", "Foliar discoloration and tissue lesions.")

    # LOW CONFIDENCE (< 60%): Actionable guidance instead of repetitive dead-end uncertainty
    if is_uncertain:
        st.markdown(
            f"""
            <div style="background-color: #fffbeb; border: 2px solid #fde68a; border-left: 6px solid #d97706; padding: 20px; border-radius: 12px; margin-bottom: 24px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="font-size: 1.3rem;">⚠️</span>
                    <h3 style="color: #92400e; margin: 0; font-size: 1.25rem; font-weight: 800;">
                        Low-Confidence Visual Match ({top_conf*100:.1f}%) — Additional Observations Recommended
                    </h3>
                </div>
                <p style="color: #78350f; font-size: 0.95rem; line-height: 1.5; margin-bottom: 12px;">
                    The top candidate match is <strong>{disease_name}</strong>, but the visual confidence score is below the strict 60% reliability threshold. 
                    Surface leaf symptoms may overlap with nutrient chlorosis, sunscald, or secondary saprophytic molds.
                </p>
                <div style="background-color: #ffffff; border: 1px solid #fef3c7; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                    <strong style="color: #92400e; font-size: 0.9rem;">📸 How to capture a more diagnostic photo for re-testing:</strong>
                    <ul style="color: #451a03; font-size: 0.88rem; margin: 6px 0 0 0; padding-left: 20px;">
                        <li><strong>Macro focus:</strong> Focus directly on the active margin (the boundary where healthy green tissue meets diseased spots).</li>
                        <li><strong>Leaf underside:</strong> Flip the leaf and inspect for powdery mildew, downy fuzz, fungal pustules, or insect pests (whiteflies/thrips/aphids).</li>
                        <li><strong>Lighting:</strong> Photograph under natural diffused daylight (morning or overcast sky) without flash glare or harsh direct shadows.</li>
                        <li><strong>Canopy position:</strong> Note whether symptoms are isolated to oldest bottom leaves (soil-splash fungi) or newest terminal growth (viruses/micro-nutrients).</li>
                    </ul>
                </div>
                <p style="color: #92400e; font-size: 0.85rem; margin: 0;">
                    ✓ <em>This observation has been logged for regional tracking (Report #{report_id}) on the Officer Surveillance Dashboard.</em>
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
                        Visual Candidate Match ({top_conf*100:.1f}%)
                    </span>
                    <span style="font-size: 0.8rem; color: #15803d; font-weight: 600;">Report #{report_id}</span>
                </div>
                <h2 style="color: #064e3b; margin: 4px 0 6px 0; font-size: 1.6rem; font-weight: 800;">{disease_name}</h2>
                <p style="color: #047857; font-size: 0.95rem; margin-bottom: 8px;">
                    <strong>Pathogen:</strong> {pathogen} &nbsp;|&nbsp; <em>{scientific_name}</em>
                </p>
                <p style="color: #1e293b; font-size: 0.9rem; margin: 0; line-height: 1.5;">
                    <strong>Observed Symptom Profile:</strong> {symptoms}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 5 STRUCTURED ACTIONABLE SECTIONS FOR THE FARMER
    st.markdown("### 📋 Actionable Farmer Disease Management Protocol")
    st.caption("Structured recommendations following Integrated Pest Management (IPM) and ICAR/KVK guidance.")

    # Section A: Possible Disease & Observed Symptoms
    with st.expander("🔍 A. Possible Disease & Observed Symptoms", expanded=True):
        st.markdown(
            f"""
            - **Candidate Disease:** **{disease_name}**
            - **Scientific Name / Group:** *{scientific_name}* ({pathogen})
            - **Target Crop:** {crop_selected}
            - **Key Field Symptoms:** {symptoms}
            - **Micro-Climate Epidemiological Risk:** Currently rated **{risk_level}** at {location_label} ({weather_info['temperature']}°C, {weather_info['humidity']}% Relative Humidity, {weather_info['precipitation']} mm rain).
            - **Diagnostic Caution:** Visual similarity to other foliar conditions (such as physiological nutrient scorch or non-pathogenic leaf spots) means physical and field confirmation is always prudent.
            """
        )

    # Section B: Immediate Steps the Farmer Can Take
    with st.expander("⚡ B. Immediate Steps the Farmer Can Take (First 24–48 Hours)", expanded=True):
        st.markdown(
            """
            1. **Sanitary Pruning:** Carefully clip and remove severely spotted or yellowed lower foliage that touches the soil. Do **not** leave clipped leaves on the ground.
            2. **Safe Disposal:** Collect diseased foliage in a clean bag and bury or burn it away from the field perimeter. **Never add diseased foliage to active compost heaps.**
            3. **Tool Sterilization:** Wash secateurs, sickles, and knives in a 70% alcohol solution or 1% sodium hypochlorite (household bleach diluted 1:9 in water) before moving between plants.
            4. **Foliage Drying:** Suspend any overhead sprinkler irrigation. Wet leaves provide the free moisture film necessary for fungal zoospores and bacteria to penetrate stomata.
            5. **Restrict Field Movement:** Avoid walking through or cultivating the crop while morning dew remains on leaves to prevent mechanical transfer of inoculum across rows.
            """
        )

    # Section C: Disease-Specific Prevention Methods
    with st.expander("🛡️ C. Disease-Specific Prevention Methods", expanded=True):
        st.markdown(f"#### Recommended Agronomic Prevention for {crop_selected} ({disease_name}):")
        cultural_points = lang_data.get("cultural", [])
        if cultural_points:
            for pt in cultural_points:
                st.markdown(f"- {pt}")
        else:
            st.markdown(
                """
                - Practice a minimum 2-year crop rotation with non-host botanical families (e.g. cereals, pulses, or brassicas).
                - Plant certified, pathogen-free seeds or transplants from reputable nurseries.
                - Utilize resistant or tolerant crop hybrids recommended by your State Agricultural University.
                - Apply reflective organic mulches (paddy straw or two-tone plastic mulch) to minimize soil splash and insect landing.
                """
            )

    # Section D: Crop Hygiene, Watering, Drainage & Monitoring Recommendations
    with st.expander("💧 D. Crop Hygiene, Watering, Drainage & Monitoring Recommendations", expanded=True):
        st.markdown(
            """
            - **Watering Management:** Utilize drip irrigation or targeted sub-surface emitters placed directly at the root zone. Irrigate in the early morning so accidental splashes dry rapidly in the sun.
            - **Drainage & Aeration:** Create raised planting beds (15–20 cm) and unblock drainage furrows to prevent water stagnation around plant crowns during monsoon showers.
            - **Air Circulation:** Maintain recommended row-to-row and plant-to-plant spacing to facilitate continuous airflow through the lower canopy.
            - **Bund Sanitation:** Keep farm bunds and boundaries completely free of wild weeds (such as *Solanum nigrum*, *Parthenium*, or wild mallows) which harbor viral vectors and fungal inoculum.
            - **Twice-Weekly Monitoring:** Walk field diagonals twice every week during early vegetative and flowering stages. Record the percentage of leaves displaying new water-soaked margins or target rings.
            """
        )

    # Section E: When to Seek Agricultural Expert Confirmation
    with st.expander("🏛️ E. When to Seek Confirmation from an Agricultural Expert", expanded=True):
        st.markdown(
            """
            **Immediate Expert Scouting Triggers — Contact your local Agriculture Officer or KVK if you observe:**
            - 🚩 **Rapid Expansion:** Spotting or necrosis spreads to more than **15–20% of the field canopy** within 48 to 72 hours.
            - 🚩 **Stem or Crown Cankers:** Dark lesions expand onto the main stem, crown, or tomato fruit calyx/cotton bolls/onion neck.
            - 🚩 **Total Wilting:** Whole plants wilt rapidly during the day despite moist soil (indicative of vascular bacterial wilt or *Fusarium*).
            - 🚩 **Vector Outbreaks:** Heavy colonies of whiteflies, thrips, or aphids congregate on the underside of young leaves.
            - 🚩 **Lack of Biocontrol Response:** Symptoms continue to progress after 4–5 days of cultural sanitation and biological biocontrol application.
            
            **How to Take a Sample to Your Local Krishi Vigyan Kendra (KVK):**
            - Collect 3–4 freshly affected leaves showing both diseased margins and adjacent healthy green tissue.
            - Place the sample in a dry, ventilated paper envelope (avoid airtight moist plastic bags which foster saprophytic rot).
            - Note the date of symptom onset, crop age, and recent spray history.
            """
        )

    # Monitored Biological & Chemical Intervention Safeguards
    st.markdown("### 🧪 Monitored Treatments & Responsible Safeguards")
    tab_bio, tab_chem, tab_safe = st.tabs([
        "🧫 Biological Biocontrols (Eco-Friendly)",
        "⚠️ Chemical Interventions (Strictly Monitored Last Resort)",
        "🦺 Operator Safety & Pre-Harvest Intervals (PHI)",
    ])

    with tab_bio:
        st.markdown("#### Biological Controls & Organic Bio-Fungicides:")
        bio_items = lang_data.get("biological", [])
        if bio_items:
            for item in bio_items:
                st.markdown(f"- {item}")
        else:
            st.markdown("- Apply *Trichoderma viride* or *Pseudomonas fluorescens* formulations during early morning or evening.")
            st.markdown("- Utilize 5% Neem Seed Kernel Extract (NSKE) as an organic deterrent against early fungal sporulation and insect vectors.")

    with tab_chem:
        st.markdown("#### Chemical Controls (Strictly As Monitored Last Resort):")
        st.error(
            "⚠️ **Responsible Chemical Usage Policy:** Chemical pesticides must **only** be deployed if disease incidence surpasses the "
            "established **Economic Threshold Level (ETL)** and biological/cultural methods prove insufficient. "
            "Never apply prophylactic calendar sprays. Consult your local KVK or Agriculture Officer for CIBRC-registered active ingredients."
        )
        chem_items = lang_data.get("chemical_last", [])
        for item in chem_items:
            st.markdown(f"- {item}")

    with tab_safe:
        st.markdown("#### Operator Health, PPE & Pre-Harvest Intervals:")
        safe_items = lang_data.get("safety_notes", [])
        for item in safe_items:
            st.markdown(f"- {item}")
        st.markdown("- **Pre-Harvest Interval (PHI):** Always observe the mandatory waiting period between application and harvest to guarantee residue-free produce for consumers.")

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
