"""
CropGuard: Early Detection of Crop Diseases & Pests
CropGuard: an open-source crop disease and pest detection tool
Main Application Entrypoint & System Hub
Includes trilingual localization (English, Hindi, Marathi) with persistent session state.
"""

import streamlit as st
import db
import model
import translations
from translations import t

# Configure page metadata
st.set_page_config(
    page_title="CropGuard | Early Crop Disease & Pest Detection",
    page_icon="logo.jpeg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize database schema and language state
db.init_db()
translations.init_language_state()
current_lang = translations.get_current_language()

# Custom CSS for modern, high-contrast, production-grade agricultural styling
st.markdown(
    """
    <style>
    /* Global Styles */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Top Header Banner */
    .main-header {
        background: linear-gradient(135deg, #064e3b 0%, #047857 55%, #059669 100%);
        padding: 28px 32px;
        border-radius: 16px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.25), 0 8px 10px -6px rgba(6, 78, 59, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .main-header h1 {
        color: #ffffff !important;
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #ecfdf5 !important;
        font-size: 1.02rem;
        margin-top: 8px;
        margin-bottom: 0;
        opacity: 0.95;
    }
    .badge-tag {
        display: inline-block;
        background-color: #fbbf24;
        color: #78350f;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.75rem;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 14px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-val {
        font-size: 2rem;
        font-weight: 800;
        color: #064e3b;
        line-height: 1.1;
    }
    .metric-lbl {
        font-size: 0.78rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 6px;
    }
    .metric-sub {
        font-size: 0.7rem;
        color: #94a3b8;
        margin-top: 2px;
    }
    
    /* Navigation / Feature Cards */
    .feature-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 22px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 250px;
        margin-bottom: 12px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
    }
    .feature-card-farmer {
        border-top: 5px solid #10b981;
    }
    .feature-card-officer {
        border-top: 5px solid #3b82f6;
    }
    .feature-card-advisory {
        border-top: 5px solid #8b5cf6;
    }
    .feature-card h4 {
        color: #0f172a !important;
        font-size: 1.18rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .feature-card p {
        color: #334155 !important;
        font-size: 0.92rem;
        line-height: 1.55;
        margin-bottom: 14px;
        flex-grow: 1;
    }
    .card-meta {
        font-size: 0.78rem;
        font-weight: 600;
        color: #059669;
        background-color: #ecfdf5;
        padding: 4px 10px;
        border-radius: 6px;
        margin-bottom: 12px;
        display: inline-block;
        border: 1px solid #d1fae5;
    }
    .card-meta-blue {
        color: #1d4ed8;
        background-color: #eff6ff;
        border: 1px solid #dbeafe;
    }
    .card-meta-purple {
        color: #6d28d9;
        background-color: #f5f3ff;
        border: 1px solid #ede9fe;
    }

    /* Disclaimer & Callout Boxes */
    .disclaimer-box {
        background-color: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 5px solid #f59e0b;
        padding: 16px 20px;
        border-radius: 10px;
        color: #92400e;
        font-size: 0.88rem;
        line-height: 1.5;
        margin-top: 24px;
    }
    
    .status-panel {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation and Language Switcher
with st.sidebar:
    st.image(
        "logo.jpeg",
        caption="CropGuard: Healthy Crops, Brighter Future",
        use_container_width=True,
    )
    
    # Persistent Language Selector
    current_lang = translations.render_language_selector(sidebar=True, key_prefix="home")

    st.markdown(f"### 📍 {t('nav_heading', current_lang)}")
    st.page_link("app.py", label=t("nav_home", current_lang), icon="🏠")
    st.page_link("pages/1_🌾_Farmer_Diagnosis.py", label=t("nav_farmer", current_lang), icon="🌾")
    st.page_link("pages/2_🛡️_Officer_Dashboard.py", label=t("nav_officer", current_lang), icon="🛡️")
    st.page_link("pages/3_📚_Disease_Advisory.py", label=t("nav_advisory", current_lang), icon="📚")
    
    st.divider()

    # System Status
    st.markdown(f"### ⚙️ {t('system_status', current_lang)}")
    engine_status = model.get_model_engine_status()
    st.markdown(
        f"""
        <div class="status-panel">
            <div style="font-size: 0.8rem; font-weight: 700; color: #0f172a; margin-bottom: 4px;">{t('vision_engine', current_lang)}</div>
            <div style="font-size: 0.82rem; font-weight: 600; color: {'#059669' if engine_status['is_neural_model_loaded'] else '#d97706'};">
                {engine_status['status_badge']}
            </div>
            <div style="font-size: 0.72rem; color: #64748b; margin-top: 4px;">
                {engine_status['engine_name']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        **Focus Crops:** 🍅 Tomato, 🌿 Cotton, 🧅 Onion  
        **Region:** Maharashtra & Central India  
        **Confidence Gate:** Strict 60% Safety Threshold
        """
    )
    
    st.divider()

    # Database Demo Actions
    st.markdown(f"### ⚡ {t('db_operations', current_lang)}")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        if st.button("📥 Seed Demo", use_container_width=True, help="Populate 32 Maharashtra district reports"):
            count = db.load_demo_data()
            st.success(f"Loaded {count} records.")
            st.rerun()
    with col_d2:
        if st.button("🗑️ Reset DB", use_container_width=True, help="Clear all records in SQLite"):
            db.delete_all_reports()
            st.warning("Database reset.")
            st.rerun()

# Main Header Banner with Logo
col_h1, col_h2 = st.columns([1, 6])
with col_h1:
    st.image("logo.jpeg", use_container_width=True)
with col_h2:
    st.markdown(
        f"""
        <div class="main-header" style="margin-bottom: 0;">
            <span class="badge-tag">{t('home_tag', current_lang)}</span>
            <h1>{t('home_title', current_lang)}</h1>
            <p>{t('home_subtitle', current_lang)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Fetch verified database statistics
stats = db.get_summary_stats()

# Statistics Section with transparent attribution
st.markdown(f"### 📊 {t('metrics_title', current_lang)}")
st.caption(t("metrics_caption", current_lang))

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-val">{stats["total_reports"]}</div>
            <div class="metric-lbl">{t("metric_total_reports", current_lang)}</div>
            <div class="metric-sub">{t("metric_total_sub", current_lang)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-val" style="color: #dc2626;">{stats["pending_verification"]}</div>
            <div class="metric-lbl">{t("metric_pending", current_lang)}</div>
            <div class="metric-sub">{t("metric_pending_sub", current_lang)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-val" style="color: #059669;">{stats["confirmed"]}</div>
            <div class="metric-lbl">{t("metric_confirmed", current_lang)}</div>
            <div class="metric-sub">{t("metric_confirmed_sub", current_lang)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-val" style="color: #d97706;">{stats["corrected"]}</div>
            <div class="metric-lbl">{t("metric_corrected", current_lang)}</div>
            <div class="metric-sub">{t("metric_corrected_sub", current_lang)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c5:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-val" style="color: #ea580c;">{stats["uncertain"]}</div>
            <div class="metric-lbl">{t("metric_uncertain", current_lang)}</div>
            <div class="metric-sub">{t("metric_uncertain_sub", current_lang)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Cards Section
st.markdown(f"### 🚀 {t('core_modules_title', current_lang)}")
st.caption(t("core_modules_caption", current_lang))

col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    st.markdown(
        f"""
        <div class="feature-card feature-card-farmer">
            <div>
                <span class="card-meta">{t('card_farmer_badge', current_lang)}</span>
                <h4>{t('card_farmer_title', current_lang)}</h4>
                <p>{t('card_farmer_desc', current_lang)}</p>
            </div>
            <div style="font-size: 0.78rem; color: #64748b; font-weight: 600;">
                ✓ Strict &lt;60% safety gate &nbsp;•&nbsp; Tomato, Cotton, Onion
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(
        "pages/1_🌾_Farmer_Diagnosis.py",
        label=t("card_farmer_btn", current_lang),
        icon="🌾",
        use_container_width=True,
    )

with col_nav2:
    st.markdown(
        f"""
        <div class="feature-card feature-card-officer">
            <div>
                <span class="card-meta card-meta-blue">{t('card_officer_badge', current_lang)}</span>
                <h4>{t('card_officer_title', current_lang)}</h4>
                <p>{t('card_officer_desc', current_lang)}</p>
            </div>
            <div style="font-size: 0.78rem; color: #64748b; font-weight: 600;">
                ✓ Active learning loop &nbsp;•&nbsp; Export CSV surveillance logs
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(
        "pages/2_🛡️_Officer_Dashboard.py",
        label=t("card_officer_btn", current_lang),
        icon="🛡️",
        use_container_width=True,
    )

with col_nav3:
    st.markdown(
        f"""
        <div class="feature-card feature-card-advisory">
            <div>
                <span class="card-meta card-meta-purple">{t('card_advisory_badge', current_lang)}</span>
                <h4>{t('card_advisory_title', current_lang)}</h4>
                <p>{t('card_advisory_desc', current_lang)}</p>
            </div>
            <div style="font-size: 0.78rem; color: #64748b; font-weight: 600;">
                ✓ Zero invented dosages &nbsp;•&nbsp; Pre-Harvest Intervals (PHI)
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(
        "pages/3_📚_Disease_Advisory.py",
        label=t("card_advisory_btn", current_lang),
        icon="📚",
        use_container_width=True,
    )

st.divider()

# System Architecture Details
st.markdown("### 🏗️ Architectural Workflow")
arch_c1, arch_c2 = st.columns([3, 2])

with arch_c1:
    st.markdown(
        """
        ```
         [ Farmer Leaf Photo ]  ──▶ [ Vision Transformer / Agro-Symptom Engine ]
                                            │
                                            ▼ Top-3 Predictions with Confidences
        [ GPS Coordinates ]    ──▶ [ Open-Meteo Live API ] ──▶ [ Rule-based Fungal/Pest Risk ]
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ Confidence Safeguard Check:                   │
                    │  - If Conf < 60% ──▶ Actionable Low-Conf Tips │
                    │  - If Conf ≥ 60% ──▶ Possible Diagnosis + IPM │
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
        - **Precision Computer Vision:** Public plant disease classification model (`linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification`) with resilient local computer-vision fallback.
        - **Safeguard Threshold:** Strict < 60% confidence gate preventing misleading pesticide purchases when diagnosis is borderline.
        - **Epidemiological Context:** Rule-based weather synthesis combining humidity (>75%), temperature (18-28°C), and rain to predict fungal spore outbursts.
        - **Responsible IPM:** Prioritizes Cultural ➔ Biological ➔ Chemical as strictly a last resort. Never generates unverified chemical quantities.
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
