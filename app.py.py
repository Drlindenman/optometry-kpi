import streamlit as st
import pandas as pd

# 1. Page Config (Clean White Dashboard Look)
st.set_page_config(page_title="KFO KPI Dashboard", layout="wide")

# Custom CSS to match the image style: White bg, Gold accents, Navy line
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: white; }
    
    /* Header with the Blue Line from your website */
    .main-title {
        color: #000000;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 36px;
        font-weight: 800;
        border-bottom: 4px solid #1a365d; /* The Blue Line */
        padding-bottom: 10px;
        margin-bottom: 25px;
    }
    
    /* Metric Cards (Gold Accents) */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 10px;
        border-top: 5px solid #b89a5b; /* Gold Top Border */
    }
    
    /* Table Styling */
    .stDataFrame { border: 1px solid #e0e0e0; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Main Title Section
st.markdown('<p class="main-title">KS FAMILY OPTOMETRY KPI</p>', unsafe_allow_html=True)
st.header("Executive Summary: January 2026")

# 2. Sidebar Management
with st.sidebar:
    st.image("https://ksfamilyoptometry.com/wp-content/uploads/2023/10/ks-family-optometry-logo.png", width=200) # Placeholder for your logo
    st.markdown("### Settings")
    diag_goal = st.slider("Diagnostic Goal %", 0.0, 20.0, 10.0)
    st.markdown("---")
    with st.expander("🔐 Payroll/Admin"):
        k_receipts = 59277.11
        bonus = max(0, (k_receipts - 55555.55) * 0.15)
        st.write(f"Dr. Keefer Bonus: **${bonus:,.2f}**")

# 3. Data Setup
data = [
    {"Doctor": "Cory Lindenman", "Location": "Winfield", "Receipts": 91256.95, "Hours": 75.5, "VF %": 6.6, "OCT %": 9.3},
    {"Doctor": "Cory Lindenman", "Location": "Andover", "Receipts": 72792.73, "Hours": 60.5, "VF %": 6.6, "OCT %": 9.3},
    {"Doctor": "Matthew Boswell", "Location": "Winfield", "Receipts": 35197.53, "Hours": 37.5, "VF %": 4.6, "OCT %": 5.8},
    {"Doctor": "Matthew Boswell", "Location": "Andover", "Receipts": 95158.09, "Hours": 90.5, "VF %": 4.6, "OCT %": 5.8},
    {"Doctor": "Michael Keefer", "Location": "Winfield", "Receipts": 43293.42, "Hours": 64.0, "VF %": 4.1, "OCT %": 12.2},
    {"Doctor": "Michael Keefer", "Location": "Andover", "Receipts": 15983.69, "Hours": 32.0, "VF %": 4.1, "OCT %": 12.2},
]
df = pd.DataFrame(data)
df['Rev/Hour'] = df['Receipts'] / df['Hours']
df = df[['Doctor', 'Location', 'Receipts', 'Hours', 'Rev/Hour', 'VF %', 'OCT %']]

# 4. Performance Table
st.subheader("January 2026 Provider Metrics")

def apply_alerts(val):
    if isinstance(val, (int, float)) and val < diag_goal:
        return 'color: #d9534f; font-weight: bold;'
    return 'color: #000000;'

styled_df = df.style.format({
    "Receipts": "${:,.2f}",
    "Hours": "{:.1f}",
    "Rev/Hour": "${:,.2f}",
    "VF %": "{:.1f}%",
    "OCT %": "{:.1f}%"
}).map(apply_alerts, subset=['VF %', 'OCT %'])

st.dataframe(styled_df, use_container_width=True, hide_index=True)

# 5. Summary Metrics (The Cards at the bottom)
st.markdown("---")
c1, c2, c3 = st.columns(3)
total_receipts = df['Receipts'].sum()
win_total = df[df['Location'] == 'Winfield']['Receipts'].sum()
and_total = df[df['Location'] == 'Andover']['Receipts'].sum()

with c1:
    st.metric("Practice Total", f"${total_receipts:,.2f}")
with c2:
    st.metric("Winfield Office", f"${win_total:,.2f}")
with c3:
    st.metric("Andover Office", f"${and_total:,.2f}")
