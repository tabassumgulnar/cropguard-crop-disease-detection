"""
CropGuard Agriculture Officer Surveillance Dashboard
CropGuard: an open-source crop disease and pest detection tool
Spatial GIS Epidemiological Map (Folium Pins & HeatMap), Disease Frequency Analytics,
Recent Reports Audit Table, and Human-in-the-Loop "Confirm / Correct Label" Active Learning Control.
"""

import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
import plotly.express as px
import db
import model

# Page Configuration
st.set_page_config(
    page_title="Officer Surveillance Dashboard | CropGuard",
    page_icon="logo.jpeg",
    layout="wide",
)

# Custom Styling
st.markdown(
    """
    <style>
    .officer-banner {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
    .officer-banner h2 {
        color: white !important;
        margin: 0;
        font-size: 1.8rem;
    }
    .expert-box {
        background-color: #f1f5f9;
        border: 2px solid #cbd5e1;
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
    <div class="officer-banner">
        <h2>🛡️ Agriculture Officer Epidemiological Dashboard</h2>
        <p style="margin: 4px 0 0 0; opacity: 0.95;">
            Maharashtra Disease Surveillance, Hotspot Heatmapping & Ground-Truth Verification
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Clean Organized Navigation Sidebar
with st.sidebar:
    st.image("logo.jpeg", use_container_width=True)
    st.markdown("### 📍 Navigation")
    st.page_link("app.py", label="Home Dashboard", icon="🏠")
    st.page_link("pages/1_🌾_Farmer_Diagnosis.py", label="Farmer Diagnostic Portal", icon="🌾")
    st.page_link("pages/2_🛡️_Officer_Dashboard.py", label="Officer GIS Dashboard", icon="🛡️")
    st.page_link("pages/3_📚_Disease_Advisory.py", label="Trilingual IPM Catalog", icon="📚")
    st.divider()
    st.markdown("### 🏛️ Surveillance Scope")
    st.caption("**State:** Maharashtra\n\n**Focus Districts:** Pune, Nashik, Jalgaon, Ahmednagar, Solapur, Nagpur, Kolhapur")
    st.divider()
    st.caption("CropGuard • Open-Source Agro-Informatics")


# Top Action Toolbar
col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 4])
with col_btn1:
    if st.button("📥 Load Demo Data (~32 Maharashtra Reports)", type="primary", use_container_width=True):
        count = db.load_demo_data()
        st.success(f"Successfully inserted {count} realistic Maharashtra field reports!")
        st.rerun()

with col_btn2:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

# Retrieve latest reports
df_reports = db.get_all_reports()

# Top KPI Summary Cards
stats = db.get_summary_stats()
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.metric("Total Submissions", stats["total_reports"])
with kpi2:
    st.metric("Pending Review", stats["pending_verification"], delta=f"{stats['pending_verification']} queue", delta_color="inverse")
with kpi3:
    st.metric("Confirmed Ground-Truth", stats["confirmed"])
with kpi4:
    st.metric("Corrected by Officer", stats["corrected"])
with kpi5:
    st.metric("Uncertain Flags (<60%)", stats["uncertain"], delta="flagged for visit", delta_color="inverse")

st.divider()

if df_reports.empty:
    st.warning("⚠️ No field reports found in the database. Click **'Load Demo Data'** above to populate sample disease reports across Maharashtra!")
    st.stop()

# Spatial Epidemiological Map
st.subheader("🗺️ Maharashtra Disease Surveillance Map & Hotspot Heatmap")
map_col_opts1, map_col_opts2 = st.columns([1, 3])

with map_col_opts1:
    map_view_mode = st.radio(
        "Map Display Layers:",
        options=["Both (Pins & Heatmap)", "Pins with Popups Only", "Heatmap Only"],
        index=0,
    )
    filter_crop_map = st.multiselect(
        "Filter by Crop:",
        options=["tomato", "cotton", "onion"],
        default=["tomato", "cotton", "onion"],
    )

map_df = df_reports[df_reports["crop"].isin(filter_crop_map)]

# Initialize Folium Map centered on Maharashtra
m = folium.Map(
    location=[19.2, 75.8],
    zoom_start=7,
    tiles="CartoDB positron",
    control_scale=True,
)

# Marker Colors by Disease Severity / Status
def get_marker_color(row):
    if row["is_uncertain"] == 1:
        return "purple"
    if row["weather_risk"] == "High":
        return "red"
    if "healthy" in row["predicted_disease"]:
        return "green"
    return "orange"

# Add HeatMap Layer if selected
if map_view_mode in ["Both (Pins & Heatmap)", "Heatmap Only"] and not map_df.empty:
    heat_data = [[row["latitude"], row["longitude"], float(row["confidence"])] for _, row in map_df.iterrows()]
    HeatMap(heat_data, radius=18, blur=14, max_zoom=10).add_to(m)

# Add Markers if selected
if map_view_mode in ["Both (Pins & Heatmap)", "Pins with Popups Only"]:
    marker_cluster = MarkerCluster().add_to(m)
    for _, r in map_df.iterrows():
        color = get_marker_color(r)
        status_badge = f"<b>Status:</b> {r['expert_status']}"
        if r["expert_label"]:
            status_badge += f" (Corrected: {r['expert_label']})"

        popup_html = f"""
        <div style="font-family: sans-serif; font-size: 12px; width: 220px;">
            <h4 style="margin: 0 0 6px 0; color: #1e3a8a;">Report #{r['id']} ({r['crop'].upper()})</h4>
            <b>Diagnosis:</b> {model.DISEASE_DISPLAY_NAMES.get(r['predicted_disease'], r['predicted_disease'])}<br>
            <b>Confidence:</b> {r['confidence']*100:.1f}%<br>
            <b>Weather Risk:</b> <span style="color: {'red' if r['weather_risk']=='High' else 'green'}; font-weight: bold;">{r['weather_risk']}</span><br>
            <b>Location:</b> {r['location_name']}<br>
            <b>Date:</b> {r['timestamp']}<br>
            {status_badge}<br>
            {'<span style="color: #b91c1c; font-weight: bold;">⚠️ Low Confidence Flag</span>' if r['is_uncertain'] else ''}
        </div>
        """
        folium.CircleMarker(
            location=[r["latitude"], r["longitude"]],
            radius=7,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"#{r['id']} - {r['crop'].title()} ({r['predicted_disease']})",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
        ).add_to(marker_cluster)

# Render map in Streamlit
st.components.v1.html(m._repr_html_(), height=500, scrolling=False)

st.caption("🔴 Red: High Weather Risk | 🟠 Orange: Active Pathogen | 🟣 Purple: Uncertain / Flagged (<60%) | 🟢 Green: Healthy Crop")

st.divider()

# Disease Analytics & Frequency Charts
st.subheader("📊 Disease Distribution & Prevalence Analytics")
chart_c1, chart_c2 = st.columns(2)

with chart_c1:
    disease_counts = df_reports["predicted_disease"].value_counts().reset_index()
    disease_counts.columns = ["Disease", "Report Count"]
    disease_counts["Display Name"] = disease_counts["Disease"].map(
        lambda x: model.DISEASE_DISPLAY_NAMES.get(x, x.replace("_", " ").title())
    )
    fig_bar = px.bar(
        disease_counts,
        x="Report Count",
        y="Display Name",
        orientation="h",
        color="Report Count",
        color_continuous_scale="Viridis",
        title="Field Incidence by Pathogen Type",
    )
    fig_bar.update_layout(yaxis={"categoryorder": "total ascending"}, height=380, margin=dict(l=10, r=10, t=40, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_c2:
    crop_counts = df_reports.groupby(["crop", "weather_risk"]).size().reset_index(name="Count")
    fig_crop = px.bar(
        crop_counts,
        x="crop",
        y="Count",
        color="weather_risk",
        barmode="group",
        title="Submissions by Crop and Weather Risk Level",
        color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981", "Unknown": "#9ca3af"},
    )
    fig_crop.update_layout(height=380, margin=dict(l=10, r=10, t=40, b=20))
    st.plotly_chart(fig_crop, use_container_width=True)

st.divider()

# Recent Reports Table
st.subheader("📋 Recent Field Submissions Audit Log")

# Table filters
f_col1, f_col2, f_col3 = st.columns(3)
with f_col1:
    status_filter = st.selectbox("Filter Verification Status:", ["All", "Pending", "Confirmed", "Corrected"])
with f_col2:
    crop_filter = st.selectbox("Filter Crop:", ["All", "Tomato", "Cotton", "Onion"])
with f_col3:
    uncertain_filter = st.selectbox("Confidence Filter:", ["All", "Uncertain Only (<60%)", "Confident (>=60%)"])

filtered_df = df_reports.copy()
if status_filter != "All":
    filtered_df = filtered_df[filtered_df["expert_status"] == status_filter]
if crop_filter != "All":
    filtered_df = filtered_df[filtered_df["crop"] == crop_filter.lower()]
if uncertain_filter == "Uncertain Only (<60%)":
    filtered_df = filtered_df[filtered_df["is_uncertain"] == 1]
elif uncertain_filter == "Confident (>=60%)":
    filtered_df = filtered_df[filtered_df["is_uncertain"] == 0]

display_table_cols = [
    "id", "timestamp", "crop", "predicted_disease", "confidence",
    "location_name", "weather_risk", "is_uncertain", "expert_status", "expert_label"
]
st.dataframe(
    filtered_df[display_table_cols],
    use_container_width=True,
    height=260,
)

# Export to CSV
csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Export Filtered Submissions to CSV",
    data=csv_data,
    file_name="cropguard_submissions_export.csv",
    mime="text/csv",
)

st.divider()

# Human-in-the-Loop "Confirm / Correct Label" Control
st.subheader("✍️ Human-in-the-Loop: Confirm / Correct Diagnostic Label")
st.markdown(
    "Agriculture Officers and KVK scientists can verify diagnoses or re-label ambiguous cases to improve the active learning retraining loop."
)

if not filtered_df.empty:
    report_options = {
        f"Report #{r['id']} | {r['crop'].title()} | {r['predicted_disease']} ({r['confidence']*100:.1f}%) | Status: {r['expert_status']}": r["id"]
        for _, r in filtered_df.iterrows()
    }
    selected_option_label = st.selectbox("Select Report to Inspect & Verify:", options=list(report_options.keys()))
    selected_id = report_options[selected_option_label]
    target_row = df_reports[df_reports["id"] == selected_id].iloc[0]

    with st.container():
        st.markdown(
            f"""
            <div class="expert-box">
                <h4 style="margin-top:0;">Audit Record: Report #{target_row['id']}</h4>
                <div style="display: flex; gap: 24px; flex-wrap: wrap;">
                    <div><strong>Timestamp:</strong> {target_row['timestamp']}</div>
                    <div><strong>Crop:</strong> {target_row['crop'].title()}</div>
                    <div><strong>AI Diagnosis:</strong> <code>{target_row['predicted_disease']}</code></div>
                    <div><strong>Confidence:</strong> {target_row['confidence']*100:.1f}%</div>
                    <div><strong>Location:</strong> {target_row['location_name']} ({target_row['latitude']}, {target_row['longitude']})</div>
                    <div><strong>Weather Risk:</strong> {target_row['weather_risk']}</div>
                    <div><strong>Current Expert Status:</strong> {target_row['expert_status']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_act1, col_act2 = st.columns(2)
        with col_act1:
            verification_action = st.radio(
                "Officer Action:",
                options=["Confirm AI Diagnosis as Correct", "Correct Disease Label (Disagrees with AI)"],
                index=0 if target_row["expert_status"] != "Corrected" else 1,
            )

        with col_act2:
            all_possible_diseases = list(model.DISEASE_DISPLAY_NAMES.keys())
            current_idx = all_possible_diseases.index(target_row["predicted_disease"]) if target_row["predicted_disease"] in all_possible_diseases else 0

            if "Correct Disease Label" in verification_action:
                chosen_expert_label = st.selectbox(
                    "Select True Clinical/Field Pathogen Label:",
                    options=all_possible_diseases,
                    format_func=lambda x: model.DISEASE_DISPLAY_NAMES.get(x, x),
                    index=current_idx,
                )
                final_status = "Corrected"
            else:
                chosen_expert_label = target_row["predicted_disease"]
                final_status = "Confirmed"

        expert_notes = st.text_area(
            "Officer Agronomic Notes & Ground-Truth Justification:",
            value=target_row["expert_notes"] or "",
            placeholder="e.g. Field inspection by AO on 28-Oct confirmed concentric rings on lower leaves; Mancozeb trial advised.",
        )

        if st.button("💾 Save Expert Verification", type="primary"):
            success = db.update_report_expert_label(
                report_id=int(target_row["id"]),
                expert_label=chosen_expert_label,
                status=final_status,
                notes=expert_notes,
            )
            if success:
                st.success(f"Report #{target_row['id']} successfully updated to '{final_status}' with label '{chosen_expert_label}'!")
                st.rerun()
            else:
                st.error("Failed to update report record.")
