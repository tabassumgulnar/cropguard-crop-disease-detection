"""
CropGuard: Early Detection of Crop Diseases & Pests
CropGuard: an open-source crop disease and pest detection tool
Main Application Entrypoint & System Hub
"""

import streamlit as st
import db

# Configure page metadata
st.set_page_config(
    page_title="CropGuard | Early Crop Disease & Pest Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize database schema
db.init_db()

# Custom CSS for polished government-grade agro-informatics styling
st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 60%, #40916c 100%);
        padding: 24px 28px;
        border-radius: 14px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    }
    .main-header h1 {
        color: #ffffff !important;
        font-size: 2.3rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #d8f3dc;
        font-size: 1.05rem;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .badge-tag {
        display: inline-block;
        background-color: #ffd166;
        color: #1b4332;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1b4332;
    }
    .metric-lbl {
        font-size: 0.85rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .feature-card {
        background-color: #f8f9fa;
        border-left: 4px solid #2d6a4f;
        padding: 16px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 12px;
    }
    .disclaimer-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-left: 5px solid #ffc107;
        padding: 14px 18px;
        border-radius: 8px;
        color: #856404;
        font-size: 0.9rem;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar with system metadata
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1592417817098-8f3d6910985c?w=600&auto=format&fit=crop&q=80",
        caption="CropGuard AI Surveillance",
        use_container_width=True,
    )
    st.markdown("### 🌾 CropGuard System Info")
    st.markdown(
        """
        **Type:** Open-Source Agro-Informatics  
        **Focus Crops:** 🍅 Tomato, 🌿 Cotton, 🧅 Onion  
        **Target Region:** Maharashtra & Central India  
        **Core Architecture:**
        - Vision Transformer / MobileNet (Hugging Face)
        - Open-Meteo Realtime Agrometeorology API
        - Trilingual IPM Advisory (EN, HI, MR)
        - SQLite Persistence & Folium Spatial Heatmap
        - Human-in-the-Loop Officer Verification
        """
    )
    st.divider()

    # Quick Demo Data Loader in Sidebar
    st.markdown("#### ⚡ Quick Actions")
    if st.button("📥 Load 32 Demo Reports (Maharashtra)", use_container_width=True):
        count = db.load_demo_data()
        st.success(f"Loaded {count} sample reports across Maharashtra!")
        st.rerun()

    if st.button("🗑️ Reset Database", use_container_width=True):
        db.delete_all_reports()
        st.warning("Database cleared.")
        st.rerun()

# Main Header
st.markdown(
    """
    <div class="main-header">
        <span class="badge-tag">CropGuard: An Open-Source Crop Disease and Pest Detection Tool</span>
        <h1>🌱 CropGuard: Early Crop Disease & Pest Detection</h1>
        <p>AI-Powered Plant Pathology, Live Weather Epidemiology, and Trilingual Integrated Pest Management (IPM)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Fetch quick metrics
stats = db.get_summary_stats()

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-val">{stats["total_reports"]}</div><div class="metric-lbl">Total Reports</div></div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f'<div class="metric-card"><div class="metric-val" style="color: #e63946;">{stats["pending_verification"]}</div><div class="metric-lbl">Pending Review</div></div>',
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f'<div class="metric-card"><div class="metric-val" style="color: #2a9d8f;">{stats["confirmed"]}</div><div class="metric-lbl">Confirmed Cases</div></div>',
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f'<div class="metric-card"><div class="metric-val" style="color: #e76f51;">{stats["corrected"]}</div><div class="metric-lbl">Expert Corrected</div></div>',
        unsafe_allow_html=True,
    )
with c5:
    st.markdown(
        f'<div class="metric-card"><div class="metric-val" style="color: #f4a261;">{stats["uncertain"]}</div><div class="metric-lbl">Uncertain (&lt;60%)</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Cards
st.subheader("🚀 Navigate to CropGuard Modules")
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🌾 1. Farmer Diagnostic Portal</h4>
            <p>Upload or snap a leaf photo, pick your crop (Tomato, Cotton, Onion), and view instant AI classification with top-3 confidence scores, live weather risk assessment, and trilingual IPM steps.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_🌾_Farmer_Diagnosis.py", label="Open Farmer Portal 👉", icon="🌾")

with col_nav2:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🛡️ 2. Officer Surveillance Dashboard</h4>
            <p>Interactive Folium spatial map with disease markers, epidemic heatmaps across Maharashtra, disease frequency charts, and a "Confirm / Correct Label" tool for expert retraining.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_🛡️_Officer_Dashboard.py", label="Open Officer Dashboard 👉", icon="🛡️")

with col_nav3:
    st.markdown(
        """
        <div class="feature-card">
            <h4>📚 3. Trilingual IPM Advisory Catalog</h4>
            <p>Direct access to scientifically-grounded Integrated Pest Management (IPM) guidelines for 10+ major diseases in English, हिन्दी (Hindi), and मराठी (Marathi), following ICAR & KVK principles.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/3_📚_Disease_Advisory.py", label="Browse Advisory Catalog 👉", icon="📚")

st.divider()

# System Architecture Details
st.subheader("🏗️ Architectural Workflow")
arch_c1, arch_c2 = st.columns([3, 2])

with arch_c1:
    st.markdown(
        """
        ```
         [ Farmer Leaf Photo ]  ──▶ [ Hugging Face Vision Model / Agro-Engine ]
                                            │
                                            ▼ Top-3 Predictions
        [ GPS Coordinates ]    ──▶ [ Open-Meteo Live API ] ──▶ [ Rule-based Fungal/Pest Risk ]
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ Confidence Check:                             │
                    │  - If Conf < 60% ──▶ "Uncertain – Consult AO" │
                    │  - If Conf ≥ 60% ──▶ Trilingual IPM Advisory  │
                    └───────────────────────────────────────────────┘
                                            │
                                            ▼
                               [ SQLite Storage / cropguard.db ]
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ Agriculture Officer GIS & Active Learning:    │
                    │  - Folium Spatial Map & Disease Heatmaps      │
                    │  - Epidemic Clustering & Alerts               │
                    │  - Human-in-the-Loop "Confirm/Correct Label"  │
                    └───────────────────────────────────────────────┘
        ```
        """
    )

with arch_c2:
    st.markdown("#### 🔬 Key Engineering Highlights")
    st.markdown(
        """
        - **Precision Computer Vision:** PlantVillage fine-tuned Hugging Face transformer models with top-3 rankings.
        - **Safeguard Threshold:** Strict < 60% confidence gate preventing misleading pesticide purchases.
        - **Epidemiological Context:** Rule-based weather synthesis combining humidity (>75%), temperature (18-28°C), and rain to predict fungal spore outbursts.
        - **Responsible IPM:** Prioritizes Cultural ➔ Biological ➔ Chemical as strictly a last resort. Never generates unverified dosages.
        - **Active Learning Ready:** Agriculture Officers can correct diagnoses, building a verified ground-truth dataset for model retraining.
        """
    )

# Official Disclaimer
st.markdown(
    """
    <div class="disclaimer-box">
        <strong>⚠️ Official ICAR / KVK Advisory Disclaimer:</strong> Guidance provided in CropGuard is strictly advisory following Integrated Pest Management (IPM) principles. Chemical pesticides should only be considered as a last resort after cultural and biological controls. Always consult your nearest Krishi Vigyan Kendra (KVK), ICAR Institute (e.g., ICAR-DOGR Pune, ICAR-CICR Nagpur), or State Department of Agriculture Extension Officer before chemical spray applications.
    </div>
    """,
    unsafe_allow_html=True,
)
