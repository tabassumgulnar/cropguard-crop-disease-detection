"""
CropGuard Trilingual Integrated Pest Management (IPM) Advisory Catalog
Comprehensive reference for 10+ diseases across Tomato, Cotton, and Onion.
Includes Cultural, Biological, Chemical (Last Resort), and Safety Notes in English, Hindi, and Marathi.
Synchronized with persistent session state language switching.
"""

import os
import json
import streamlit as st
import translations
from translations import t

st.set_page_config(
    page_title="IPM Advisory Catalog | CropGuard",
    page_icon="logo.jpeg",
    layout="wide",
)

# Initialize language session state
translations.init_language_state()
lang_code = translations.get_current_language()

st.markdown(
    """
    <style>
    .advisory-header {
        background: linear-gradient(135deg, #064e3b 0%, #047857 55%, #059669 100%);
        padding: 24px 28px;
        border-radius: 14px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(6, 78, 59, 0.15);
    }
    .advisory-header h2 {
        color: white !important;
        margin: 0;
        font-size: 2rem;
        font-weight: 800;
    }
    .disease-banner {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 6px solid #10b981;
        padding: 16px 20px;
        border-radius: 10px;
        margin: 14px 0;
    }
    .disclaimer-card {
        background-color: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 5px solid #d97706;
        padding: 16px 20px;
        border-radius: 10px;
        color: #92400e;
        margin-top: 28px;
        font-size: 0.88rem;
        line-height: 1.5;
    }
    .ipm-framework-box {
        background-color: #ffffff;
        border: 1px solid #d1fae5;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 22px;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_advisory_json():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "advisory.json")
    if not os.path.exists(path):
        path = "advisory.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_advisory_json()
disclaimer_dict = data.get("disclaimer", {})
diseases_dict = data.get("diseases", {})

# Clean Organized Navigation Sidebar
with st.sidebar:
    st.image("logo.jpeg", use_container_width=True)
    
    # Persistent Language Selector
    lang_code = translations.render_language_selector(sidebar=True, key_prefix="advisory_sidebar")

    st.markdown(f"### 📍 {t('nav_heading', lang_code)}")
    st.page_link("app.py", label=t("nav_home", lang_code), icon="🏠")
    st.page_link("pages/1_🌾_Farmer_Diagnosis.py", label=t("nav_farmer", lang_code), icon="🌾")
    st.page_link("pages/2_🛡️_Officer_Dashboard.py", label=t("nav_officer", lang_code), icon="🛡️")
    st.page_link("pages/3_📚_Disease_Advisory.py", label=t("nav_advisory", lang_code), icon="📚")
    st.divider()
    st.markdown("### 📖 IPM Philosophy")
    st.caption("1. Cultural Sanity\n2. Biological Defense\n3. Chemical Strictly as Last Resort\n4. Zero Invented Dosages")
    st.divider()
    st.caption(t("footer_credit", lang_code))

st.markdown(
    f"""
    <div class="advisory-header">
        <h2>{t('advisory_banner_title', lang_code)}</h2>
        <p style="margin: 6px 0 0 0; opacity: 0.95; font-size: 1.05rem;">
            {t('advisory_banner_subtitle', lang_code)}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Overarching IPM Framework
st.markdown(
    """
    <div class="ipm-framework-box">
        <h4 style="color: #064e3b; margin: 0 0 8px 0; font-size: 1.05rem;">🌿 Integrated Pest Management (IPM) Guiding Philosophy</h4>
        <div style="font-size: 0.88rem; color: #334155; line-height: 1.55;">
            CropGuard structures plant pathology management into three strictly prioritized tiers:
            <strong>Tier 1: Preventive Agronomic & Cultural Controls</strong> (seed selection, field hygiene, drip watering, crop rotation) 
            ➔ <strong>Tier 2: Biological & Bio-Pesticide Defenses</strong> (beneficial microorganisms, botanical repellents, pheromone monitoring) 
            ➔ <strong>Tier 3: Monitored Chemical Intervention</strong> (applied only when pest incidence exceeds verified Economic Threshold Levels, adhering strictly to CIBRC guidelines and Pre-Harvest Intervals).
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Filters Row
c1, c2, c3 = st.columns([1.5, 1.5, 2])
with c1:
    lang_labels = ["English", "हिन्दी (Hindi)", "मराठी (Marathi)"]
    lang_codes = ["en", "hi", "mr"]
    code_to_idx = {"en": 0, "hi": 1, "mr": 2}
    current_idx = code_to_idx.get(lang_code, 0)
    chosen_label = st.selectbox(
        "🌐 Language / भाषा / भाषा निवडा:",
        options=lang_labels,
        index=current_idx,
        key="advisory_top_lang",
    )
    new_lang = lang_codes[lang_labels.index(chosen_label)]
    if new_lang != lang_code:
        translations.set_current_language(new_lang)
        st.rerun()

with c2:
    crop_filter = st.selectbox(
        t("filter_crop_label", lang_code),
        options=["All Crops", "Tomato", "Cotton", "Onion"],
        format_func=lambda x: {"All Crops": t("all_crops", lang_code), "Tomato": "🍅 Tomato", "Cotton": "🌿 Cotton", "Onion": "🧅 Onion"}.get(x, x),
        index=0,
    )

with c3:
    search_query = st.text_input(t("search_advisory_label", lang_code), placeholder="e.g. blight, curl, Alternaria")

# Filter logic
filtered_keys = []
for d_key, d_info in diseases_dict.items():
    crop = d_info.get("crop", "")
    if crop_filter != "All Crops" and crop != crop_filter.lower():
        continue

    lang_entry = d_info.get(lang_code, d_info.get("en", {}))
    searchable_str = f"{d_key} {d_info.get('scientific_name', '')} {lang_entry.get('name', '')} {lang_entry.get('symptoms', '')}".lower()

    if search_query.strip():
        if search_query.lower() not in searchable_str:
            continue
    filtered_keys.append(d_key)

st.caption(f"Showing **{len(filtered_keys)}** disease advisories matching criteria.")

# Render Advisories
for d_key in filtered_keys:
    d_info = diseases_dict[d_key]
    crop = d_info.get("crop", "crop").title()
    sci_name = d_info.get("scientific_name", "")
    lang_data = d_info.get(lang_code, d_info.get("en", {}))
    disease_localized_name = translations.get_disease_name(d_key, lang_code)

    crop_badge = "🍅 Tomato" if crop == "Tomato" else ("🌿 Cotton" if crop == "Cotton" else "🧅 Onion")

    with st.expander(f"{crop_badge} — {disease_localized_name}", expanded=(len(filtered_keys) <= 3)):
        st.markdown(
            f"""
            <div class="disease-banner">
                <h3 style="margin: 0 0 6px 0; color: #064e3b; font-size: 1.25rem;">{disease_localized_name}</h3>
                <p style="margin: 0 0 6px 0; color: #047857; font-size: 0.92rem;">
                    <strong>Pathogen:</strong> {lang_data.get('pathogen', '')} &nbsp;|&nbsp; <em>{sci_name}</em>
                </p>
                <p style="margin: 0; color: #1e293b; font-size: 0.9rem; line-height: 1.5;">
                    <strong>Diagnostic Symptoms:</strong> {lang_data.get('symptoms', '')}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Clear separation between Preventive Measures and Monitored Treatments
        tab_prev, tab_treat = st.tabs([
            t("part1_tab", lang_code),
            t("part2_tab", lang_code),
        ])

        with tab_prev:
            col_c, col_b = st.columns(2)
            with col_c:
                st.markdown("##### 🌱 1. Cultural & Agronomic Prevention")
                for item in lang_data.get("cultural", []):
                    st.markdown(f"- {item}")

            with col_b:
                st.markdown("##### 🧫 2. Biological Biocontrols & Bio-Pesticides")
                for item in lang_data.get("biological", []):
                    st.markdown(f"- {item}")

        with tab_treat:
            col_ch, col_s = st.columns(2)
            with col_ch:
                st.markdown("##### 🧪 1. Chemical Interventions (Strictly After ETL Breached)")
                st.warning(t("chem_warning", lang_code))
                for item in lang_data.get("chemical_last", []):
                    st.markdown(f"- {item}")

            with col_s:
                st.markdown("##### 🦺 2. Operator Safety, PPE & Pre-Harvest Intervals (PHI)")
                for item in lang_data.get("safety_notes", []):
                    st.markdown(f"- {item}")
                st.markdown(f"- **{t('phi_note', lang_code)}**")

# Regulatory Notice
disclaimer_body = disclaimer_dict.get(lang_code, disclaimer_dict.get("en", ""))
st.markdown(
    f"""
    <div class="disclaimer-card">
        <strong>📜 Official Agriculture Advisory Disclaimer:</strong><br>
        {disclaimer_body}
    </div>
    """,
    unsafe_allow_html=True,
)
