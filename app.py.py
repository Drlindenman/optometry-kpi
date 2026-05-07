import streamlit as st
import pandas as pd

# 1. SETUP - KFO Branding
st.set_page_config(page_title="KFO KPI Dashboard", layout="wide")

# Navy: #1a365d | Gold: #b89a5b
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #1a365d !important; font-family: 'Helvetica Neue', sans-serif; font-weight: bold; }
    h2 { color: #b89a5b !important; }
    .stMetric { border: 1px solid #1a365d; padding: 15px; border-radius: 10px; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("KS FAMILY OPTOMETRY KPI")
st.header("January 2026 Performance Report")

# 2. SIDEBAR
diag_goal = st.sidebar.slider("Diagnostic Goal %", 0.0, 20.0, 10.0)
st.sidebar.markdown("---")
with st.sidebar.expander("🔐 Admin / Payroll Details"):
    keefer_receipts = 59277.11 
    keefer_bonus = max(0, (keefer_receipts - 55555.55) * 0.15)
    st.write(f"**Dr. Keefer Jan Bonus:** ${keefer_bonus:,.2f}")

# 3. JANUARY 2026 DATA
data = [
    {"Doctor": "Cory Lindenman", "Location": "Winfield", "Receipts": 91256.95, "Hours": 75.5, "VF %": 6.6, "OCT %": 9.3},
    {"Doctor": "Cory Lindenman", "Location": "Andover", "Receipts": 72792.73, "Hours": 60.5, "VF %": 6.6, "OCT %": 9.3},
    {"Doctor": "Matthew Boswell", "Location": "Winfield", "Receipts": 35197.53, "Hours": 37.5, "VF %": 4.6, "OCT %": 5.8},
    {"Doctor": "Matthew Boswell", "Location": "Andover", "Receipts": 95158.09, "Hours": 90.5, "VF %": 4.6, "OCT %": 5.8},
    {"Doctor": "Michael Keefer", "Location": "Winfield", "Receipts": 43293.42, "Hours": 64.0, "VF %": 4.1, "OCT %": 12.2},
    {"Doctor": "Michael Keefer", "Location": "Andover", "Receipts": 15983.69, "Hours": 32.0, "VF %": 4.1, "OCT %": 12.2},
]

df = pd.DataFrame(data)

# 4. CALCULATION & SEQUENCE (Receipts -> Hours -> Rev/Hour)
df['Rev/Hour'] = df['Receipts'] / df['Hours']
df = df[['Doctor', 'Location', 'Receipts', 'Hours', 'Rev/Hour', 'VF %', 'OCT %']]

# 5. STYLING FUNCTION - Red Alerts
def apply_style(val):
    if isinstance(val, (int, float)) and val < diag_goal:
        return 'color: #d9534f; font-weight: bold; background-color: #fff5f5;'
    return ''

st.subheader("Provider Metrics: January 2026")

# 6. FORMATTING - Force $ and % Symbols
styled_df = df.style.format({
    "Receipts": "${:,.2f}",
    "Hours": "{:.1f}",
    "Rev/Hour": "${:,.2f}",
    "VF %": "{:.1f}%",
    "OCT %": "{:.1f}%"
}).map(apply_style, subset=['VF %', 'OCT %'])

st.dataframe(styled_df, use_container_width=True)

# 7. TOTALS
st.markdown("---")
win_total = df[df['Location'] == 'Winfield']['Receipts'].sum()
and_total = df[df['Location'] == 'Andover']['Receipts'].sum()

col1, col2 = st.columns(2)
with col1:
    st.metric("Winfield Total (Jan 2026)", f"${win_total:,.2f}")
with col2:
    st.metric("Andover Total (Jan 2026)", f"${and_total:,.2f}")
