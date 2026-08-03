import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="KS FAMILY OPTOMETRY KPI", layout="wide")

# 2. Custom CSS - Black, Gold, and White Aesthetic (Matching Mockup)
st.markdown("""
    <style>
    /* Force main app background to clean white */
    .stApp { 
        background-color: #FFFFFF !important; 
    }
    
    /* Main Title Styling with Gold Bottom Accent Line */
    .kfo-title {
        color: #000000;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 34px;
        font-weight: 800;
        border-bottom: 4px solid #B89A5B; /* Gold Accent Line */
        padding-bottom: 10px;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }
    
    /* Subheaders */
    h2, h3 {
        color: #000000 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
    }
    
    /* Metric Cards with Gold Top Accent (Black & Gold Look) */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 18px;
        border-radius: 8px;
        border-top: 5px solid #B89A5B; /* Gold Top Accent Bar */
        box-shadow: 0px 2px 5px rgba(0,0,0,0.04);
    }
    
    /* Metric Values & Labels */
    div[data-testid="stMetricLabel"] > label {
        color: #555555 !important;
        font-size: 14px;
        font-weight: 600;
    }
    
    div[data-testid="stMetricValue"] > div {
        color: #000000 !important;
        font-weight: 800;
    }
    
    /* Table Container Styling */
    .stDataFrame {
        border: 1px solid #E0E0E0;
        border-radius: 8px;
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

# 5. January 2026 Raw Data
data = [
    {"Doctor": "Cory Lindenman", "Location": "Winfield", "Receipts": 91256.95, "Hours": 75.5, "VF %": 6.6, "OCT %": 9.3},
    {"Doctor": "Cory Lindenman", "Location": "Andover", "Receipts": 72792.73, "Hours": 60.5, "VF %": 6.6, "OCT %": 9.3},
    {"Doctor": "Matthew Boswell", "Location": "Winfield", "Receipts": 35197.53, "Hours": 37.5, "VF %": 4.6, "OCT %": 5.8},
    {"Doctor": "Matthew Boswell", "Location": "Andover", "Receipts": 95158.09, "Hours": 90.5, "VF %": 4.6, "OCT %": 5.8},
    {"Doctor": "Michael Keefer", "Location": "Winfield", "Receipts": 43293.42, "Hours": 64.0, "VF %": 4.1, "OCT %": 12.2},
    {"Doctor": "Michael Keefer", "Location": "Andover", "Receipts": 15983.69, "Hours": 32.0, "VF %": 4.1, "OCT %": 12.2},
]

df = pd.DataFrame(data)

# Calculate Revenue per Hour and lock column order
df['Rev/Hour'] = df['Receipts'] / df['Hours']
df = df[['Doctor', 'Location', 'Receipts', 'Hours', 'Rev/Hour', 'VF %', 'OCT %']]

# 6. Styling Logic for Low Metrics
def apply_alerts(val):
    if isinstance(val, (int, float)) and val < diag_goal:
        return 'color: #D32F2F; font-weight: bold;'
    return 'color: #000000;'

st.subheader("January 2026 Provider Metrics")

# Format currency and percentages
styled_df = df.style.format({
    "Receipts": "${:,.2f}",
    "Hours": "{:.1f}",
    "Rev/Hour": "${:,.2f}",
    "VF %": "{:.1f}%",
    "OCT %": "{:.1f}%"
}).map(apply_alerts, subset=['VF %', 'OCT %'])

# Render table
st.dataframe(styled_df, use_container_width=True, hide_index=True)

# 7. Summary Cards (Black & Gold Look)
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
