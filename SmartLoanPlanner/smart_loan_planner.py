'''
Given a loan amount, interest rate, and term, this app calculates the monthly payment and generates a loan payoff schedule. It also allows users to explore the impact of making extra payments or adjusting the monthly payment to reach a target payoff date.
I need this to determine the required monthly payment to reach a target payoff date, also the monthly payment calculation.
and allow users to test different payment amounts using a slider. The app will display the results in a table and provide visualizations of the loan balance over time.
'''


import streamlit as st
import pandas as pd
from datetime import date
'''For new loans

Uses:
• Loan Amount
• Interest Rate
• Term

Calculates:
• Monthly Payment
• Amortization Schedule
• Target Payoff Scenarios
'''
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Smart Loan Planner",
    page_icon="💰",
    layout="wide"
)

# ==========================================================
# STYLING
# ==========================================================

st.markdown("""
<style>
[data-testid="stMetricLabel"] {
    font-size:18px;
}

[data-testid="stMetricValue"] {
    font-size:26px;
}

h1 {
    font-size:42px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 Smart Loan Planner")
st.caption(
    "Calculate monthly payments, payoff schedules, extra payment scenarios, and target payoff dates."
)

# ==========================================================
# HELPERS
# ==========================================================

def add_months(dt, months):
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1

    days_in_month = [
        31,
        29 if year % 4 == 0 and (
            year % 100 != 0 or year % 400 == 0
        ) else 28,
        31,30,31,30,31,31,30,31,30,31
    ]

    day = min(dt.day, days_in_month[month - 1])

    return date(year, month, day)


def format_currency(value):
    return f"${value:,.2f}"


def calculate_monthly_payment(
    loan_amount,
    annual_rate,
    term_months
):
    monthly_rate = annual_rate / 12

    if monthly_rate == 0:
        return round(
            loan_amount / term_months,
            2
        )

    payment = (
        loan_amount *
        (
            monthly_rate *
            (1 + monthly_rate) ** term_months
        )
        /
        (
            (1 + monthly_rate) ** term_months - 1
        )
    )

    return round(payment, 2)


def calculate_required_payment(
    balance,
    annual_rate,
    months
):
    monthly_rate = annual_rate / 12

    if monthly_rate == 0:
        return round(
            balance / months,
            2
        )

    payment = (
        balance *
        (
            monthly_rate *
            (1 + monthly_rate) ** months
        )
        /
        (
            (1 + monthly_rate) ** months - 1
        )
    )

    return round(payment, 2)


def build_schedule(
    loan_amount,
    annual_rate,
    payment_amount,
    start_date
):

    monthly_rate = annual_rate / 12

    balance = loan_amount

    month = 1

    total_interest = 0.0

    rows = []

    payoff_date = None

    while balance > 0:

        payment_date = add_months(
            start_date,
            month - 1
        )

        interest = round(
            balance * monthly_rate,
            2
        )

        principal = round(
            min(
                balance,
                payment_amount - interest
            ),
            2
        )

        if principal <= 0:
            raise ValueError(
                "Payment too low for interest rate."
            )

        actual_payment = round(
            principal + interest,
            2
        )

        balance = round(
            max(
                0,
                balance - principal
            ),
            2
        )

        total_interest += interest

        rows.append(
            {
                "Month": month,
                "Payment Date": payment_date,
                "Payment": actual_payment,
                "Principal": principal,
                "Interest": interest,
                "Balance": balance
            }
        )

        if balance == 0:
            payoff_date = payment_date

        month += 1

    return {
        "Rows": rows,
        "Payoff Month": month - 1,
        "Payoff Date": payoff_date,
        "Total Interest": round(
            total_interest,
            2
        ),
        "Total Paid": round(
            sum(
                r["Payment"]
                for r in rows
            ),
            2
        ),
        "Payment Amount": round(
            payment_amount,
            2
        )
    }

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("Loan Inputs")

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=1.0,
        value=25000.0,
        step=1000.0
    )

    annual_rate_pct = st.number_input(
        "Interest Rate (%)",
        min_value=0.0,
        value=6.5,
        step=0.01
    )

    term_years = st.number_input(
        "Loan Term (Years)",
        min_value=1,
        value=5
    )

    extra_payment = st.number_input(
        "Extra Monthly Payment",
        min_value=0.0,
        value=100.0,
        step=25.0
    )

    use_target = st.checkbox(
        "Target Payoff Date",
        value=True
    )

    target_date = None

    if use_target:

        target_date = st.date_input(
            "Target Payoff Date",
            value=date(
                date.today().year + 3,
                date.today().month,
                1
            )
        )

annual_rate = annual_rate_pct / 100

term_months = term_years * 12

today = date.today()

# ==========================================================
# BASELINE
# ==========================================================

monthly_payment = calculate_monthly_payment(
    loan_amount,
    annual_rate,
    term_months
)

baseline = build_schedule(
    loan_amount,
    annual_rate,
    monthly_payment,
    today
)

extra_schedule = build_schedule(
    loan_amount,
    annual_rate,
    monthly_payment + extra_payment,
    today
)

# ==========================================================
# TARGET
# ==========================================================

required_payment = None
required_extra = None
target_schedule = None
slider_schedule = None

if target_date:

    months_until_target = (
        (target_date.year - today.year) * 12
        + (target_date.month - today.month)
        + 1
    )

    required_payment = calculate_required_payment(
        loan_amount,
        annual_rate,
        months_until_target
    )

    required_extra = round(
        required_payment - monthly_payment,
        2
    )

    target_schedule = build_schedule(
        loan_amount,
        annual_rate,
        required_payment,
        today
    )

    st.subheader("Target Payoff Slider")

    slider_payment = st.slider(
        "Test Monthly Payment",
        min_value=float(monthly_payment),
        max_value=float(required_payment * 1.5),
        value=float(required_payment),
        step=25.0
    )

    slider_schedule = build_schedule(
        loan_amount,
        annual_rate,
        slider_payment,
        today
    )

# ==========================================================
# METRICS
# ==========================================================

st.subheader("Loan Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Loan Amount",
    format_currency(loan_amount)
)

c2.metric(
    "Monthly Payment",
    format_currency(monthly_payment)
)

c3.metric(
    "Interest Rate",
    f"{annual_rate_pct:.2f}%"
)

c4.metric(
    "Term",
    f"{term_years} Years"
)

# ==========================================================
# SCENARIOS
# ==========================================================

st.subheader("Scenario Comparison")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown("### Baseline")

    st.metric(
        "Payment",
        format_currency(
            baseline["Payment Amount"]
        )
    )

    st.metric(
        "Payoff Date",
        str(baseline["Payoff Date"])
    )

    st.metric(
        "Total Interest",
        format_currency(
            baseline["Total Interest"]
        )
    )

with c2:

    st.markdown("### Extra Payment")

    st.metric(
        "Payment",
        format_currency(
            extra_schedule["Payment Amount"]
        )
    )

    st.metric(
        "Months Saved",
        baseline["Payoff Month"]
        - extra_schedule["Payoff Month"]
    )

    st.metric(
        "Interest Saved",
        format_currency(
            baseline["Total Interest"]
            - extra_schedule["Total Interest"]
        )
    )

if target_schedule:

    with c3:

        st.markdown("### Target Date")

        st.metric(
            "Required Payment",
            format_currency(
                required_payment
            )
        )

        st.metric(
            "Required Extra",
            format_currency(
                required_extra
            )
        )

        st.metric(
            "Payoff Date",
            str(target_schedule["Payoff Date"])
        )

if slider_schedule:

    target_met = (
        slider_schedule["Payoff Date"]
        <= target_date
    )

    months_saved = (
        baseline["Payoff Month"]
        - slider_schedule["Payoff Month"]
    )

    years_saved = months_saved // 12
    remaining_months = months_saved % 12
    
    payoff_months = slider_schedule["Payoff Month"]

    payoff_years = payoff_months // 12
    remaining_months = payoff_months % 12

    with c4:

        st.markdown("### Slider Test")

        st.metric(
            "Payment",
            format_currency(slider_payment)
        )

        st.metric(
            "Payoff Date",
            str(slider_schedule["Payoff Date"])
        )
        st.metric(
            "Payoff Term",
            f"{payoff_years} Years {remaining_months} Months"
        )
        st.metric(
            "Target Achieved",
            "✅ YES" if target_met else "❌ NO"
        )

        st.metric(
            "Months Saved",
            months_saved
        )

        st.metric(
            "Years Saved",
            f"{years_saved}y {remaining_months}m"
        )

        st.metric(
            "Interest Saved",
            format_currency(
                baseline["Total Interest"]
                - slider_schedule["Total Interest"]
            )
        )
        
  



# ==========================================================
# SCHEDULE
# ==========================================================

df = pd.DataFrame(
    baseline["Rows"]
)

st.subheader(
    "Amortization Schedule"
)

st.dataframe(
    df,
    use_container_width=True
)

# ==========================================================
# BALANCE CHART
# ==========================================================

chart_df = df.set_index(
    "Payment Date"
)[["Balance"]]

st.subheader("Balance Over Time")

st.line_chart(chart_df)

# ==========================================================
# EXPORT
# ==========================================================

csv = df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "⬇️ Download Amortization Schedule",
    csv,
    file_name="loan_schedule.csv",
    mime="text/csv"
)