import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="KS FAMILY OPTOMETRY KPI", layout="wide")

# 2. Custom CSS - Black, Gold, and White Aesthetic
st.markdown("""
    <style>
    /* Main app background */
    .stApp { 
        background-color: #FFFFFF !important; 
    }
    
    /* Title with Gold Accent Line */
    .kfo-title {
        color: #000000;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 34px;
        font-weight: 800;
        border-bottom: 4px solid #B89A5B; /* Gold Accent Bar */
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Headers */
    h2, h3 {
        color: #000000 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
    }
    
    /* Gold Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 18px;
        border-radius: 8px;
        border-top: 5px solid #B89A5B;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.04);
    }
    
    div[data-testid="stMetricLabel"] > label {
        color: #555555 !important;
        font-size: 14px;
        font-weight: 600;
    }
    
    div[data-testid="stMetricValue"] > div {
        color: #000000 !important;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Main Header
st.markdown('<div class="kfo-title">KS FAMILY OPTOMETRY KPI</div>', unsafe_allow_html=True)
st.header("Executive Summary: January 2026")

# 4. Sidebar Controls & Admin Drawer
with st.sidebar:
    st.markdown("### Management Settings")
    diag_goal = st.slider("Diagnostic Goal %", 0.0, 20.0, 10.0)
    
    st.markdown("---")
    with st.expander("🔐 Admin (Keefer Bonus)"):
        keefer_receipts = 59277.11
        keefer_bonus = max(0, (keefer_receipts - 55555.55) * 0.15)
        st.write(f"Dr. Keefer Bonus: **${keefer_bonus:,.2f}**")

# 5. Data Setup
data = [
    {"Doctor": "Cory Lindenman", "Location": "Winfield", "Receipts": 91256.95, "Hours": 75.5, "VF %": 6.6, "OCT %": 9.3},
    {"Doctor": "Cory Lindenman", "Location": "Andover", "Receipts": 72792.73, "Hours": 60.5, "VF %": 6.6, "OCT %": 9.3},
    {"Doctor": "Matthew Boswell", "Location": "Winfield", "Receipts": 35197.53, "Hours": 37.5, "VF %": 4.6, "OCT %": 5.8},
    {"Doctor": "Matthew Boswell", "Location": "Andover", "Receipts": 95158.09, "Hours": 90.5, "VF %": 4.6, "OCT %": 5.8},
    {"Doctor": "Michael Keefer", "Location": "Winfield", "Receipts": 43293.42, "Hours": 64.0, "VF %": 4.1, "OCT %": 12.2},
    {"Doctor": "Michael Keefer", "Location": "Andover", "Receipts": 15983.69, "Hours": 32.0, "VF %": 4.1, "OCT %": 12.2},
]

df = pd.DataFrame(data)

# Calculate Revenue per Hour
df['Rev/Hour'] = df['Receipts'] / df['Hours']

# Reorder columns for display table
table_df = df[['Doctor', 'Location', 'Receipts', 'Hours', 'Rev/Hour', 'VF %', 'OCT %']]

# 6. Low Goal Alert Styling
def apply_alerts(val):
    if isinstance(val, (int, float)) and val < diag_goal:
        return 'color: #D32F2F; font-weight: bold;'
    return 'color: #000000;'

st.subheader("January 2026 Provider Metrics Table")

styled_df = table_df.style.format({
    "Receipts": "${:,.2f}",
    "Hours": "{:.1f}",
    "Rev/Hour": "${:,.2f}",
    "VF %": "{:.1f}%",
    "OCT %": "{:.1f}%"
}).map(apply_alerts, subset=['VF %', 'OCT %'])

st.dataframe(styled_df, use_container_width=True, hide_index=True)

# 7. Clear Monthly Totals (Labeled by Location)
st.markdown("---")
st.subheader("Monthly Totals by Location")

total_receipts = df['Receipts'].sum()
win_total = df[df['Location'] == 'Winfield']['Receipts'].sum()
and_total = df[df['Location'] == 'Andover']['Receipts'].sum()

c1, c2, c3 = st.columns(3)
with c1:
    st.metric(label="Combined Practice Total (Jan 2026)", value=f"${total_receipts:,.2f}")
with c2:
    st.metric(label="Winfield Location Total (Jan 2026)", value=f"${win_total:,.2f}")
with c3:
    st.metric(label="Andover Location Total (Jan 2026)", value=f"${and_total:,.2f}")

# 8. Interactive Performance Visualizations
st.markdown("---")
st.subheader("Performance Analytics Graphs")

col_graph1, col_graph2 = st.columns(2)

# Graph 1: Revenue per Location by Doctor
with col_graph1:
    fig_location = px.bar(
        df, 
        x="Location", 
        y="Receipts", 
        color="Doctor",
        title="Revenue Breakdown by Location & Doctor",
        labels={"Receipts": "Total Receipts ($)", "Location": "Clinic Location"},
        color_discrete_sequence=['#1a365d', '#B89A5B', '#4A5568'], # Navy, Gold, Charcoal
        barmode="stack"
    )
    fig_location.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_location, use_container_width=True)

# Graph 2: Revenue Per Hour by Doctor
with col_graph2:
    fig_rev_hour = px.bar(
        df, 
        x="Doctor", 
        y="Rev/Hour", 
        color="Location",
        title="Revenue per Hour by Doctor & Location",
        labels={"Rev/Hour": "Revenue / Hour ($)", "Doctor": "Provider"},
        color_discrete_sequence=['#B89A5B', '#1a365d'],
        barmode="group"
    )
    fig_rev_hour.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_rev_hour, use_container_width=True)
