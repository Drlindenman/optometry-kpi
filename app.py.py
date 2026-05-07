import streamlit as st
import pandas as pd

# 1. Page Config (Clean White Background)
st.set_page_config(page_title="KS FAMILY OPTOMETRY KPI", layout="wide")

# Custom CSS for the "Blue Line" look and clean white background
st.markdown("""
    <style>
    /* Force entire page to white background */
    .main { background-color: white !important; }
    
    /* Style H1: Add the Blue Line */
    h1 {
        color: black !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
        border-bottom: 3px solid #1a365d; /* THE BLUE LONG LINE */
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Style H2: Reporting Date */
    h2 { color: black !important; font-family: sans-serif; }
    
    /* Metrics: White background with minimal black text */
    .stMetric { border: none !important; color: black; background-color: white; }
    
    /* Ensure all background elements are white */
    .stApp { background-color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("KS FAMILY OPTOMETRY KPI")
st.header("Executive KPI Report: January 2026")

# 2. SIDEBAR - Admin Features
with st.sidebar.expander("🔐 Admin (Keefer Bonus)"):
    # Bonus is hidden until expanded
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

# 5. STYLING FUNCTION - Red Text for Metrics below 10%
def apply_style(val):
    if isinstance(val, (int, float)) and val < 10.0:
        return 'color: #D32F2F; font-weight: bold;'
    return 'color: black;'

st.subheader("January 2026 Provider Metrics")

# 6. FORMATTING - Force $ and % Symbols
styled_df = df.style.format({
    "Receipts": "${:,.2f}",
    "Hours": "{:.1f}",
    "Rev/Hour": "${:,.2f}",
    "VF %": "{:.1f}%",
    "OCT %": "{:.1f}%"
}).map(apply_style, subset=['VF %', 'OCT %'])

# Using dataframe for better visual consistency
st.dataframe(styled_df, use_container_width=True)

# 7. TOTALS SUMMARY
st.markdown("---")
win_total = df[df['Location'] == 'Winfield']['Receipts'].sum()
and_total = df[df['Location'] == 'Andover']['Receipts'].sum()

col1, col2 = st.columns(2)
with col1:
    st.metric("Winfield Total (Jan 2026)", f"${win_total:,.2f}")
with col2:
    st.metric("Andover Total (Jan 2026)", f"${and_total:,.2f}")
