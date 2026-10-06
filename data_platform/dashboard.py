import sys, os
from pathlib import Path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import duckdb
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="CyberPulse | Real-Time Cloud SIEM & Threat Lakehouse",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# HIGH-END SOC CYBERSECURITY DESIGN SYSTEM (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background-color: #070b14 !important;
    background-image: radial-gradient(circle at 10% 10%, #0d1527 0%, #060911 60%, #04060a 100%) !important;
    color: #f8fafc !important;
}

section[data-testid="stSidebar"] {
    background-color: #0c1322 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding-top: 1.5rem !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p {
    color: #f1f5f9 !important;
}

section[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #141e33 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #f8fafc !important;
    font-weight: 500 !important;
}

div[data-baseweb="popover"] ul {
    background-color: #141e33 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

div[data-baseweb="popover"] li {
    color: #f8fafc !important;
}

div[data-baseweb="popover"] li:hover {
    background-color: #1e293b !important;
}

/* Action Buttons */
button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 10px 16px !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    transition: all 0.2s ease !important;
}

button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
}

button[kind="secondary"] {
    background: #141e33 !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 10px 16px !important;
    transition: all 0.2s ease !important;
}

button[kind="secondary"]:hover {
    background: #1e293b !important;
    border-color: rgba(99, 102, 241, 0.5) !important;
    color: #ffffff !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    background-color: #0c1322 !important;
    padding: 6px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 6px !important;
    padding: 8px 16px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: #cbd5e1 !important;
    border: none !important;
    background: transparent !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35) !important;
}

/* Banner */
.top-banner {
    background: linear-gradient(135deg, rgba(23, 33, 56, 0.9) 0%, rgba(11, 17, 30, 0.98) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    padding: 22px 28px;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(16px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

.banner-title {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 40%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.banner-subtitle {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-top: 5px;
    font-weight: 400;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 5px 12px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}

.pulse-dot {
    width: 7px;
    height: 7px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* Metric Cards */
.kpi-card {
    background: linear-gradient(145deg, rgba(23, 33, 56, 0.85) 0%, rgba(13, 19, 34, 0.98) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(12px);
    transition: transform 0.2s ease, border-color 0.2s ease;
    margin-bottom: 12px;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4);
}

.kpi-card-emerald { border-top: 3px solid #10b981; }
.kpi-card-indigo  { border-top: 3px solid #6366f1; }
.kpi-card-amber   { border-top: 3px solid #f59e0b; }
.kpi-card-cyan    { border-top: 3px solid #06b6d4; }
.kpi-card-rose    { border-top: 3px solid #f43f5e; }

.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.kpi-title {
    color: #94a3b8;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    white-space: nowrap;
}

.kpi-pill {
    font-size: 0.68rem;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 4px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.kpi-pill-emerald { background: rgba(16, 185, 129, 0.18); color: #34d399; }
.kpi-pill-indigo  { background: rgba(99, 102, 241, 0.18); color: #a5b4fc; }
.kpi-pill-amber   { background: rgba(245, 158, 11, 0.18); color: #fcd34d; }
.kpi-pill-cyan    { background: rgba(6, 182, 212, 0.18); color: #67e8f9; }
.kpi-pill-rose    { background: rgba(244, 63, 94, 0.18); color: #fda4af; }

.kpi-value {
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #f8fafc;
    line-height: 1.2;
    font-family: 'JetBrains Mono', 'Plus Jakarta Sans', monospace;
}

.kpi-value-emerald { color: #34d399; }
.kpi-value-indigo  { color: #a5b4fc; }
.kpi-value-amber   { color: #fcd34d; }
.kpi-value-cyan    { color: #67e8f9; }
.kpi-value-rose    { color: #fda4af; }

.kpi-footer {
    margin-top: 7px;
    font-size: 0.74rem;
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 6px;
}

.kpi-tag-success { color: #34d399; font-weight: 600; }
.kpi-tag-danger  { color: #fb7185; font-weight: 600; }

.glass-panel {
    background: linear-gradient(145deg, rgba(20, 28, 48, 0.75) 0%, rgba(11, 16, 28, 0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(12px);
    margin-bottom: 18px;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATABASE DATA ACCESS (Zero Locking)
# -----------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "cyberpulse_warehouse.duckdb")

def load_warehouse_data():
    if not os.path.exists(DB_PATH):
        return None, None, None
    con = duckdb.connect(DB_PATH, read_only=False)
    try:
        inc_df = con.execute("SELECT * FROM cyberpulse_analytics.fct_security_incidents;").df()
        att_df = con.execute("SELECT * FROM cyberpulse_analytics.spark_attacker_intel;").df()
        exp_df = con.execute("SELECT * FROM cyberpulse_analytics.fct_asset_exposure;").df()
        return inc_df, att_df, exp_df
    finally:
        con.close()

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
<div style="padding: 6px 0 16px 0;">
    <h2 style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin: 0;">
        SIEM Sensor Console
    </h2>
    <p style="color: #94a3b8; font-size: 0.78rem; margin: 4px 0 0 0;">Network flow ingestion & threat telemetry</p>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("Emit Security Event Stream (80 Logs)", use_container_width=True, type="primary"):
    with st.spinner("Emitting network packet flows & running CEP threat scoring..."):
        from streaming.consumer_to_lakehouse import sink_security_stream_to_lakehouse
        sink_security_stream_to_lakehouse(80)
        from analytics_dbt.run_dbt import run_dbt_models
        run_dbt_models()
        from batch.spark_threat_aggregation_job import run_spark_threat_batch
        run_spark_threat_batch()
    st.sidebar.success("80 events streamed & threat intelligence refreshed.")
    st.rerun()

if st.sidebar.button("Run Spark Threat Aggregation", use_container_width=True):
    with st.spinner("Executing PySpark distributed IP threat profiling..."):
        from batch.spark_threat_aggregation_job import run_spark_threat_batch
        run_spark_threat_batch()
    st.sidebar.success("Spark attacker profiling finished.")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='font-size: 0.85rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;'>Traffic Filters</h3>", unsafe_allow_html=True)

# Check DB exists
if not os.path.exists(DB_PATH):
    st.warning("Warehouse database not initialized.")
    if st.button("Initialize CyberPulse Pipeline", type="primary"):
        with st.spinner("Executing end-to-end pipeline initialization..."):
            from scripts.run_pipeline import run_entire_pipeline
            run_entire_pipeline()
        st.rerun()
    st.stop()

inc_df, att_df, exp_df = load_warehouse_data()
if inc_df is None or len(inc_df) == 0:
    st.info("No security telemetry found. Run the pipeline to initialize data.")
    st.stop()

# Interactive Filters
selected_action = st.sidebar.selectbox("Firewall Action", ["ALL", "ALLOW", "DENY"])
selected_severity = st.sidebar.selectbox("Threat Severity", ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
selected_protocol = st.sidebar.selectbox("Protocol", ["ALL"] + sorted(inc_df['protocol'].unique().tolist()))

# Filter Data
filtered_inc = inc_df.copy()
if selected_action != "ALL":
    filtered_inc = filtered_inc[filtered_inc['action'] == selected_action]
if selected_severity != "ALL":
    filtered_inc = filtered_inc[filtered_inc['severity'] == selected_severity]
if selected_protocol != "ALL":
    filtered_inc = filtered_inc[filtered_inc['protocol'] == selected_protocol]

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background: rgba(20, 30, 50, 0.7); padding: 12px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08);">
    <div style="color: #94a3b8; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Infrastructure Status</div>
    <div style="margin-top: 8px; font-size: 0.8rem; display: flex; flex-direction: column; gap: 6px;">
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Kafka:</b> <span style="color:#94a3b8;">VPC Log Stream</span></div>
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">CEP Engine:</b> <span style="color:#94a3b8;">Sliding Window Threat</span></div>
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Lakehouse:</b> <span style="color:#94a3b8;">MinIO Parquet</span></div>
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Batch:</b> <span style="color:#94a3b8;">PySpark IP Threat Intel</span></div>
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Engine:</b> <span style="color:#94a3b8;">DuckDB / BigQuery</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TOP HERO BANNER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="top-banner">
    <div>
        <h1 class="banner-title">CyberPulse Command Center</h1>
        <p class="banner-subtitle">
            Enterprise Cloud SIEM Lakehouse • Real-Time MITRE ATT&CK Threat Radar • Autonomous SOC Defense
        </p>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        <div class="status-pill">
            <span class="pulse-dot"></span>
            SOC SENSOR STREAM ACTIVE
        </div>
        <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.35); color: #a5b4fc; padding: 5px 12px; border-radius: 6px; font-size: 0.78rem; font-weight: 700;">
            DEFENSE SLA: REAL-TIME
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# EXECUTIVE KPI METRICS
# -----------------------------------------------------------------------------
total_events = len(filtered_inc)
blocked_events = len(filtered_inc[filtered_inc['action'] == 'DENY'])
block_rate = (blocked_events / total_events * 100) if total_events > 0 else 0
threat_alerts_cnt = len(filtered_inc[filtered_inc['is_threat'] == True])
total_bytes = int(filtered_inc['bytes_transferred'].sum())
mb_ingested = round(total_bytes / (1024 * 1024), 2)
avg_threat_score = float(filtered_inc['threat_score'].mean()) if total_events > 0 else 0

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
<div class="kpi-card kpi-card-emerald">
    <div class="kpi-header">
        <span class="kpi-title">Network Events</span>
        <span class="kpi-pill kpi-pill-emerald">FLOWS</span>
    </div>
    <div class="kpi-value kpi-value-emerald">{total_events:,}</div>
    <div class="kpi-footer">
        <span class="kpi-tag-success">Active Ingestion</span>
        <span>VPC Flow & Auth Logs</span>
    </div>
</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
<div class="kpi-card kpi-card-indigo">
    <div class="kpi-header">
        <span class="kpi-title">Firewall Block Rate</span>
        <span class="kpi-pill kpi-pill-indigo">BLOCKED</span>
    </div>
    <div class="kpi-value kpi-value-indigo">{block_rate:.1f}%</div>
    <div class="kpi-footer">
        <span class="kpi-tag-success">{blocked_events} blocked</span>
        <span>Dropped at perimeter</span>
    </div>
</div>
""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
<div class="kpi-card kpi-card-rose">
    <div class="kpi-header">
        <span class="kpi-title">Active Threat Alerts</span>
        <span class="kpi-pill kpi-pill-rose">THREATS</span>
    </div>
    <div class="kpi-value kpi-value-rose">{threat_alerts_cnt}</div>
    <div class="kpi-footer">
        <span class="kpi-tag-danger">{(threat_alerts_cnt / total_events * 100 if total_events > 0 else 0):.1f}% Flagged</span>
        <span>Brute force & port scans</span>
    </div>
</div>
""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
<div class="kpi-card kpi-card-cyan">
    <div class="kpi-header">
        <span class="kpi-title">Bandwidth Analyzed</span>
        <span class="kpi-pill kpi-pill-cyan">DATA</span>
    </div>
    <div class="kpi-value kpi-value-cyan">{mb_ingested} <span style="font-size: 0.9rem; color: #94a3b8;">MB</span></div>
    <div class="kpi-footer">
        <span style="color: #22d3ee; font-weight: 600;">Deep Packet Trace</span>
        <span>Inbound & Outbound</span>
    </div>
</div>
""", unsafe_allow_html=True)

with c5:
    st.markdown(f"""
<div class="kpi-card kpi-card-amber">
    <div class="kpi-header">
        <span class="kpi-title">Mean Threat Index</span>
        <span class="kpi-pill kpi-pill-amber">INDEX</span>
    </div>
    <div class="kpi-value kpi-value-amber">{avg_threat_score:.1f}</div>
    <div class="kpi-footer">
        <span style="color: #fbbf24; font-weight: 600;">0-100 Score</span>
        <span>Autonomous risk weighting</span>
    </div>
</div>
""", unsafe_allow_html=True)

def get_dark_plotly_layout(height=340):
    return dict(
        height=height,
        margin=dict(l=15, r=15, t=35, b=15),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color="#94a3b8", size=12),
        hoverlabel=dict(bgcolor="#1e293b", font_color="#f8fafc", font_size=12)
    )

# -----------------------------------------------------------------------------
# TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "MITRE ATT&CK Threat Radar",
    "Threat Actor IP Intelligence",
    "Protected Asset Exposure Matrix",
    "Packet Trace & Network Stream",
    "SIEM Lakehouse Architecture"
])

# TAB 1: RADAR
with tab1:
    c_left, c_right = st.columns([1, 1])
    
    with c_left:
        st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
        Attack Distribution by MITRE Technique
    </h3>
    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Classification of detected threats against industry standard threat tactics</p>
</div>
""", unsafe_allow_html=True)
        threat_only = filtered_inc[filtered_inc['is_threat'] == True]
        if len(threat_only) > 0:
            tech_df = threat_only.groupby("mitre_technique_id")['event_id'].count().reset_index()
            tech_df.columns = ["Technique", "Detections"]
            fig_pie = px.pie(
                tech_df,
                names="Technique",
                values="Detections",
                hole=0.55,
                color="Technique",
                color_discrete_sequence=["#f43f5e", "#f59e0b", "#6366f1", "#06b6d4", "#ec4899"]
            )
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#0b0f19', width=2))
            )
            fig_pie.update_layout(**get_dark_plotly_layout(height=310))
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.success("No active threats detected in the current filter.")

    with c_right:
        st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
        Geographic Threat Origin Distribution
    </h3>
    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Volume of attack vectors originating from external countries</p>
</div>
""", unsafe_allow_html=True)
        geo_df = filtered_inc.groupby("source_country")['event_id'].count().reset_index().sort_values(by="event_id", ascending=False)
        geo_df.columns = ["Country", "Attempts"]
        fig_geo = px.bar(
            geo_df,
            x="Country",
            y="Attempts",
            color="Attempts",
            color_continuous_scale=["#312e81", "#6366f1", "#f43f5e"]
        )
        fig_geo.update_layout(
            xaxis=dict(title=None, showgrid=False),
            yaxis=dict(title="Inbound Attempts", showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            coloraxis_showscale=False,
            **get_dark_plotly_layout(height=310)
        )
        st.plotly_chart(fig_geo, use_container_width=True)

# TAB 2: ATTACKER INTEL
with tab2:
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(244, 63, 94, 0.12) 0%, rgba(15, 23, 42, 0.4) 100%); border: 1px solid rgba(244, 63, 94, 0.3); border-radius: 12px; padding: 18px 22px; margin-bottom: 20px;">
    <h4 style="color: #fb7185; margin: 0 0 6px 0; font-size: 1.05rem; font-weight: 700;">
        Apache Spark Attacker IP Intelligence Profiling (Gold Model)
    </h4>
    <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0; line-height: 1.5;">
        Autonomous entity profiling aggregating attempt volume, firewall drop percentage, attacked port diversity, and peak threat score to drive automated IP blocklisting.
    </p>
</div>
""", unsafe_allow_html=True)

    if len(att_df) > 0:
        st.dataframe(
            att_df.style.format({
                'total_attempts': '{:,}',
                'blocked_attempts': '{:,}',
                'block_rate_pct': '{:.1f}%',
                'peak_threat_score': '{:.0f}',
                'total_bytes_transferred': '{:,} B'
            }),
            use_container_width=True
        )

# TAB 3: ASSET EXPOSURE
with tab3:
    st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
        Protected Enterprise Assets Exposure & Target Risk
    </h3>
    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Correlation of network flow destinations against protected Tier-1 and Tier-2 assets</p>
</div>
""", unsafe_allow_html=True)

    if len(exp_df) > 0:
        st.dataframe(
            exp_df.style.format({
                'total_inbound_connections': '{:,}',
                'blocked_connections': '{:,}',
                'security_incidents_flagged': '{:,}',
                'max_threat_score_seen': '{:.0f}'
            }),
            use_container_width=True
        )

# TAB 4: PACKET TRACE
with tab4:
    st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
        Atomic Security Packet Traces & Forensic Stream
    </h3>
    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Raw network flow events partitioned in Lakehouse (Parquet) and reconciled in dbt marts</p>
</div>
""", unsafe_allow_html=True)

    st.dataframe(
        filtered_inc.sort_values(by="event_timestamp", ascending=False).head(100)[[
            'event_id', 'event_timestamp', 'source_ip', 'source_country',
            'destination_ip', 'targeted_asset_name', 'destination_port',
            'protocol', 'action', 'threat_score', 'severity', 'threat_reasons'
        ]].style.format({
            'destination_port': '{:.0f}',
            'threat_score': '{:.0f}'
        }),
        use_container_width=True
    )

# TAB 5: ARCHITECTURE
with tab5:
    st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin: 0 0 8px 0;">
        End-to-End Enterprise Cloud SIEM Lakehouse Stack
    </h3>
    <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.6;">
        CyberPulse was architected to ingest high-velocity VPC and security log streams, running real-time Complex Event Processing before multi-year partitioned lakehouse storage.
    </p>
</div>
""", unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px; height: 100%;">
    <div style="color: #6366f1; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">1. Ingestion & Streaming</div>
    <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.5;">
        • <b>Apache Kafka (KRaft)</b>: High-volume ingestion of VPC Flow, SSH & WAF logs.<br>
        • <b>dltHub Pipeline</b>: Syncs MITRE ATT&CK definitions and Asset Catalogs.<br>
        • <b>Complex Event Processing</b>: Sliding window threat detection at ingestion.
    </p>
</div>
""", unsafe_allow_html=True)
    with col_s2:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px; height: 100%;">
    <div style="color: #06b6d4; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">2. Multi-Tier Lakehouse</div>
    <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.5;">
        • <b>Bronze Layer</b>: Raw partitioned Parquet logs in MinIO for SOC2 compliance.<br>
        • <b>PySpark Distributed Engine</b>: Aggregates Attacker Entity profiles & blocklists.<br>
        • <b>Gold Ledger</b>: Reconciled threat intelligence datasets for security dispatch.
    </p>
</div>
""", unsafe_allow_html=True)
    with col_s3:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px; height: 100%;">
    <div style="color: #10b981; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">3. Analytics & Orchestration</div>
    <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.5;">
        • <b>dbt (Data Build Tool)</b>: Dimensional star schema for security incident marts.<br>
        • <b>Data Quality Tests</b>: Automated assertions on packet volumes and schemas.<br>
        • <b>Kestra DAGs</b>: Declarative orchestrator for end-to-end security workflows.
    </p>
</div>
""", unsafe_allow_html=True)
