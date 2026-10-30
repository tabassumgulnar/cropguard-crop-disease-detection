"""
CropGuard Trilingual Integrated Pest Management (IPM) Advisory Catalog
Comprehensive reference for 10+ diseases across Tomato, Cotton, and Onion.
Includes Cultural, Biological, Chemical (Last Resort), and Safety Notes in English, Hindi, and Marathi.
"""

import os
import json
import streamlit as st

st.set_page_config(
    page_title="IPM Advisory Catalog | CropGuard",
    page_icon="📚",
    layout="wide",
)

st.markdown(
    """
    <style>
    .advisory-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
    .disease-banner {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 6px solid #2563eb;
        padding: 16px 20px;
        border-radius: 8px;
        margin: 16px 0;
    }
    .disclaimer-card {
        background-color: #fefce8;
        border: 1px solid #fde047;
        border-left: 5px solid #eab308;
        padding: 14px 18px;
        border-radius: 8px;
        color: #713f12;
        margin-top: 24px;
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

st.markdown(
    """
    <div class="advisory-header">
        <h2 style="color:white; margin:0;">📚 Trilingual IPM Disease & Pest Advisory Catalog</h2>
        <p style="margin:4px 0 0 0; opacity:0.95;">
            Integrated Pest Management (IPM) Protocols • Cultural • Biological • Chemical-Last • Safety
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Filters Row
c1, c2, c3 = st.columns([1.5, 1.5, 2])
with c1:
    lang_choice = st.selectbox(
        "Select Language / भाषा चुनें / भाषा निवडा:",
        options=["English (en)", "हिन्दी (hi)", "मराठी (mr)"],
        index=0,
    )
    lang_code = "en"
    if "हिन्दी" in lang_choice:
        lang_code = "hi"
    elif "मराठी" in lang_choice:
        lang_code = "mr"

with c2:
    crop_filter = st.selectbox(
        "Filter by Crop:",
        options=["All Crops", "Tomato", "Cotton", "Onion"],
        index=0,
    )

with c3:
    search_query = st.text_input("🔎 Search by symptom, disease, or pathogen name:", placeholder="e.g. blight, curl, Alternaria")

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

    crop_badge = "🍅 Tomato" if crop == "Tomato" else ("🌿 Cotton" if crop == "Cotton" else "🧅 Onion")

    with st.expander(f"{crop_badge} — {lang_data.get('name', d_key)}", expanded=(len(filtered_keys) <= 3)):
        st.markdown(
            f"""
            <div class="disease-banner">
                <h3 style="margin: 0 0 6px 0; color: #1e3a8a;">{lang_data.get('name')}</h3>
                <p style="margin: 0 0 8px 0; color: #475569;">
                    <strong>Pathogen:</strong> {lang_data.get('pathogen', '')} | <em>{sci_name}</em>
                </p>
                <p style="margin: 0; color: #1e293b;">
                    <strong>Diagnostic Symptoms:</strong> {lang_data.get('symptoms', '')}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_c, col_b = st.columns(2)
        with col_c:
            st.markdown("##### 🌱 1. Cultural & Preventative Practices")
            for item in lang_data.get("cultural", []):
                st.markdown(f"- {item}")

        with col_b:
            st.markdown("##### 🧫 2. Biological & Organic Controls")
            for item in lang_data.get("biological", []):
                st.markdown(f"- {item}")

        col_ch, col_s = st.columns(2)
        with col_ch:
            st.markdown("##### 🧪 3. Chemical Controls (Strictly As Last Resort)")
            st.warning("⚠️ Never apply chemical sprays without exceeding Economic Threshold Levels (ETL).")
            for item in lang_data.get("chemical_last", []):
                st.markdown(f"- {item}")

        with col_s:
            st.markdown("##### 🦺 4. Operator Safety & Pre-Harvest Interval")
            for item in lang_data.get("safety_notes", []):
                st.markdown(f"- {item}")

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
