import streamlit as st
import pandas as pd

st.set_page_config(page_title="KPI Dashboard", layout="wide")
st.title("📊 Optometry Practice Command Center")

# Actual January 2026 Data
data = [
    {"Doctor": "Cory Lindenman", "Role": "Owner", "Receipts": 164049.68, "VF %": 6.6, "OCT %": 9.3, "G2211 %": 0.0},
    {"Doctor": "Matthew Boswell", "Role": "Owner", "Receipts": 130355.62, "VF %": 4.6, "OCT %": 5.8, "G2211 %": 0.0},
    {"Doctor": "Michael Keefer", "Role": "Associate", "Receipts": 59277.11, "VF %": 4.1, "OCT %": 12.2, "G2211 %": 0.0}
]
df = pd.DataFrame(data)

# KPI Calculations
keefer_bonus = max(0, (59277.11 - 55555.55) * 0.15)

col1, col2 = st.columns(2)
col1.metric("Total Practice Receipts", "$353,682.41")
col2.metric("Dr. Keefer Jan Bonus", f"${keefer_bonus:,.2f}")

st.subheader("Clinical Performance (Red = Below Goal)")
st.dataframe(df)

st.info("Summer 2026: Dr. Holman pre-configured with $10k base and $66,666.67 bonus tier.")