import streamlit as st
from datetime import date

st.set_page_config(page_title="Enhanced Loan Payoff Analysis V2", layout="wide")

st.title("🚀 GEORGE STREAMLIT V2")
st.success("You are running the NEW V2 version")

with st.sidebar:
    st.header("Loan Inputs")
    balance = st.number_input("Outstanding Balance", value=24527.85)
    rate = st.number_input("Interest Rate (%)", value=5.29)
    payment = st.number_input("Current Payment", value=1075.29)
    target_date = st.date_input("Target Payoff Date", value=date(2027,12,24))

st.subheader("Recommended Payment")
recommended_payment = 1420.44
st.metric("Recommended Payment", f"${recommended_payment:,.2f}")

if "payment_slider" not in st.session_state:
    st.session_state.payment_slider = recommended_payment

if st.button("Use Recommended Payment"):
    st.session_state.payment_slider = recommended_payment

slider_payment = st.slider(
    "Test Monthly Payment",
    min_value=float(payment),
    max_value=2500.0,
    value=float(st.session_state.payment_slider),
    step=25.0
)

col1,col2,col3,col4 = st.columns(4)
col1.metric("Slider Payment", f"${slider_payment:,.2f}")
col2.metric("Slider Extra", f"${slider_payment-payment:,.2f}")
col3.metric("Target Date", str(target_date))
col4.metric("Balance", f"${balance:,.2f}")

if slider_payment >= recommended_payment:
    st.success("✅ Target Date Reached")
else:
    st.error("❌ Target Date Missed")

st.line_chart({
    "Baseline":[24527,22000,19500,17000,14500,12000],
    "Slider":[24527,21000,17500,14000,10000,5000]
})

st.info("This is the downloadable V2 starter with banner, recommended payment card, button, and payment slider.")
