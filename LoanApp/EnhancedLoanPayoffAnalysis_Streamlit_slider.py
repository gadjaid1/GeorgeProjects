import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Enhanced Loan Payoff Analysis", layout="wide")
st.markdown("""
<style>
[data-testid="stMetricLabel"] {
    font-size: 18px;
}

[data-testid="stMetricValue"] {
    font-size: 26px;
}

h1 {
    font-size: 45px !important;
}

h2 {
    font-size: 23px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 GEORGE STREAMLIT V2")
st.success("Enhanced Loan Payoff Analysis + Slider Version") 

# ============================================================
# Helper Functions
# ============================================================

def add_months(dt, months):
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1
    days_in_month = [
        31,
        29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    ]
    day = min(dt.day, days_in_month[month - 1])
    return date(year, month, day)


def calculate_required_payment(balance, annual_rate, months):
    monthly_rate = annual_rate / 12

    if months <= 0:
        return round(balance, 2)

    if monthly_rate == 0:
        return round(balance / months, 2)

    payment = (
        balance
        * (monthly_rate * (1 + monthly_rate) ** months)
        / ((1 + monthly_rate) ** months - 1)
    )

    return round(payment, 2)


def calculate_loan_start_date(maturity_date, original_term_months):
    return add_months(maturity_date, -(original_term_months - 1))


def calculate_current_month(loan_start_date, original_term_months, as_of_date):
    for month in range(1, original_term_months + 1):
        payment_date = add_months(loan_start_date, month - 1)
        if payment_date >= as_of_date:
            return month
    return original_term_months


def count_payments_through_target(loan_start_date, current_month, target_date):
    if target_date is None:
        return None

    payment_count = 0
    month = current_month

    while True:
        payment_date = add_months(loan_start_date, month - 1)
        if payment_date > target_date:
            break
        payment_count += 1
        month += 1
        if payment_count > 600:
            break

    return payment_count


def build_schedule(start_month, loan_start_date, starting_balance, annual_rate, payment_amount):
    balance = starting_balance
    total_interest = 0.00
    rows = []
    month = start_month
    payoff_month = None
    payoff_date = None

    while balance > 0:
        payment_date = add_months(loan_start_date, month - 1)
        interest = round(balance * annual_rate / 12, 2)
        principal = min(balance, payment_amount - interest)

        if principal <= 0:
            raise ValueError(
                "Payment amount is too low to reduce principal. "
                "Increase the payment amount or check the interest rate."
            )

        actual_payment = round(principal + interest, 2)
        balance = round(max(0, balance - principal), 2)
        total_interest += interest

        rows.append({
            "Month": month,
            "Payment Date": payment_date,
            "Payment": actual_payment,
            "Interest": round(interest, 2),
            "Principal": round(principal, 2),
            "Balance": round(balance, 2)
        })

        if balance == 0:
            payoff_month = month
            payoff_date = payment_date

        month += 1

    return {
        "Rows": rows,
        "Payoff Month": payoff_month,
        "Payoff Date": payoff_date,
        "Total Interest": round(total_interest, 2),
        "Total Paid": round(sum(r["Payment"] for r in rows), 2),
        "Payment Amount": round(payment_amount, 2)
    }


def format_currency(value):
    if value is None:
        return "N/A"
    return f"${value:,.2f}"


def run_analysis(
    original_loan_amount,
    outstanding_loan_amount,
    annual_rate,
    standard_payment,
    extra_payment,
    maturity_date,
    original_term_months,
    as_of_date,
    target_payoff_date,
    slider_payment=None,
    show_full_history=False
):
    target_date_specified = target_payoff_date is not None

    loan_start_date = calculate_loan_start_date(maturity_date, original_term_months)

    current_month = calculate_current_month(
        loan_start_date,
        original_term_months,
        as_of_date
    )

    months_completed = current_month - 1
    remaining_term_months = original_term_months - current_month + 1
    
    if show_full_history:
        schedule_start_month = 1
        schedule_start_balance = original_loan_amount
    else:
        schedule_start_month = current_month
        schedule_start_balance = outstanding_loan_amount

    baseline_payment = standard_payment
    fixed_extra_payment = round(standard_payment + extra_payment, 2)

    baseline = build_schedule(
        schedule_start_month,
        loan_start_date,
        schedule_start_balance,
        annual_rate,
        baseline_payment
    )

    fixed_extra = build_schedule(
        schedule_start_month,
        loan_start_date,
        schedule_start_balance,
        annual_rate,
        fixed_extra_payment
    )

    target = None
    slider = None
    target_payment_count = None
    required_target_payment = None
    required_target_extra_payment = None
    target_achieved = None
    slider_target_achieved = None

    if target_date_specified:
        target_payment_count = count_payments_through_target(
            loan_start_date,
            current_month,
            target_payoff_date
        )

        required_target_payment = calculate_required_payment(
            outstanding_loan_amount,
            annual_rate,
            target_payment_count
        )

        required_target_extra_payment = round(
            max(0, required_target_payment - standard_payment),
            2
        )

        target = build_schedule(
            schedule_start_month,
            loan_start_date,
            schedule_start_balance,
            annual_rate,
            required_target_payment
        )
        target_achieved = target["Payoff Date"] <= target_payoff_date

        if slider_payment is not None:
            slider = build_schedule(
                schedule_start_month,
                loan_start_date,
                schedule_start_balance,
                annual_rate,
                slider_payment
            )
            slider_target_achieved = slider["Payoff Date"] <= target_payoff_date

    max_rows = max(
        len(baseline["Rows"]),
        len(fixed_extra["Rows"]),
        len(target["Rows"]) if target is not None else 0,
        len(slider["Rows"]) if slider is not None else 0
    )

    combined_rows = []

    for i in range(max_rows):
        base_row = baseline["Rows"][i] if i < len(baseline["Rows"]) else None
        extra_row = fixed_extra["Rows"][i] if i < len(fixed_extra["Rows"]) else None
        target_row = target["Rows"][i] if target is not None and i < len(target["Rows"]) else None
        slider_row = slider["Rows"][i] if slider is not None and i < len(slider["Rows"]) else None

        month = None
        payment_date = None

        for row in (base_row, extra_row, target_row, slider_row):
            if row is not None:
                month = row["Month"]
                payment_date = row["Payment Date"]
                break

        base_balance = base_row["Balance"] if base_row else 0.00
        extra_balance = extra_row["Balance"] if extra_row else 0.00
        target_balance = target_row["Balance"] if target_row else None
        slider_balance = slider_row["Balance"] if slider_row else None

        combined_rows.append({
            "Month": month,
            "Payment Date": payment_date,
            "Baseline Payment": base_row["Payment"] if base_row else 0.00,
            "Baseline Balance": base_balance,
            "Fixed Extra Payment": extra_row["Payment"] if extra_row else 0.00,
            "Fixed Extra Balance": extra_balance,
            "Fixed Extra Advance": round(base_balance - extra_balance, 2),
            "Required Target Payment": target_row["Payment"] if target_row else None,
            "Required Target Balance": target_balance,
            "Slider Payment": slider_row["Payment"] if slider_row else None,
            "Slider Balance": slider_balance,
            "Slider Advance": round(base_balance - slider_balance, 2) if slider_balance is not None else None
        })

    fixed_months_saved = baseline["Payoff Month"] - fixed_extra["Payoff Month"]
    fixed_interest_saved = round(baseline["Total Interest"] - fixed_extra["Total Interest"], 2)

    if target is not None:
        target_months_saved = baseline["Payoff Month"] - target["Payoff Month"]
        target_interest_saved = round(baseline["Total Interest"] - target["Total Interest"], 2)
    else:
        target_months_saved = None
        target_interest_saved = None

    if slider is not None:
        slider_months_saved = baseline["Payoff Month"] - slider["Payoff Month"]
        slider_interest_saved = round(baseline["Total Interest"] - slider["Total Interest"], 2)
        slider_extra_payment = round(slider_payment - standard_payment, 2)
    else:
        slider_months_saved = None
        slider_interest_saved = None
        slider_extra_payment = None

    return {
        "Target Date Specified": target_date_specified,
        "Target Achieved": target_achieved,
        "Slider Target Achieved": slider_target_achieved,
        "Loan Start Date": loan_start_date,
        "Maturity Date": maturity_date,
        "As Of Date": as_of_date,
        "Original Loan Amount": original_loan_amount,
        "Outstanding Loan Amount": outstanding_loan_amount,
        "Annual Rate": annual_rate,
        "Original Term Months": original_term_months,
        "Months Completed": months_completed,
        "Current Month": current_month,
        "Remaining Term Months": remaining_term_months,
        "Standard Payment": standard_payment,
        "Extra Payment": extra_payment,
        "Payment With Fixed Extra": fixed_extra_payment,
        "Target Payoff Date": target_payoff_date,
        "Required Target Payment": required_target_payment,
        "Required Target Extra Payment": required_target_extra_payment,
        "Target Payment Count": target_payment_count,
        "Baseline": baseline,
        "Fixed Extra": fixed_extra,
        "Fixed Months Saved": fixed_months_saved,
        "Fixed Interest Saved": fixed_interest_saved,
        "Target": target,
        "Target Months Saved": target_months_saved,
        "Target Interest Saved": target_interest_saved,
        "Slider": slider,
        "Slider Payment": slider_payment,
        "Slider Extra Payment": slider_extra_payment,
        "Slider Months Saved": slider_months_saved,
        "Slider Interest Saved": slider_interest_saved,
        "Combined Rows": combined_rows
    }


# ============================================================
# Streamlit UI
# ============================================================


st.caption("Compare baseline payoff, fixed extra payment, required target payoff, and a payment slider.")

with st.sidebar:
    st.header("Loan Parameters")

    original_loan_amount = st.number_input(
        "Original Loan Amount",
        min_value=0.0,
        value=66000.00,
        step=500.00,
        format="%.2f"
    )

    outstanding_loan_amount = st.number_input(
        "Outstanding Loan Amount",
        min_value=0.0,
        value=24527.85,
        step=100.00,
        format="%.2f"
    )

    annual_rate_percent = st.number_input(
        "Annual Rate (%)",
        min_value=0.0,
        value=5.29,
        step=0.01,
        format="%.3f"
    )

    standard_payment = st.number_input(
        "Standard Monthly Payment",
        min_value=0.0,
        value=1075.29,
        step=25.00,
        format="%.2f"
    )

    extra_payment = st.number_input(
        "Fixed Extra Payment",
        min_value=0.0,
        value=150.00,
        step=25.00,
        format="%.2f"
    )

    maturity_date = st.date_input(
        "Maturity Date",
        value=date(2028, 6, 24)
    )

    original_term_months = st.number_input(
        "Original Term Months",
        min_value=1,
        value=73,
        step=1
    )

    as_of_date = st.date_input(
        "As Of Date",
        value=date.today()
    )

    show_full_history = st.checkbox(
        "Show Full Loan History",
        value=False
    )

    use_target_date = st.checkbox(
        "Calculate payment needed for target payoff date",
        value=True
    )

    target_payoff_date = None
    if use_target_date:
        target_payoff_date = st.date_input(
            "Target Payoff Date",
            value=date(2027, 12, 24)
        )

annual_rate = annual_rate_percent / 100

# Payment slider appears when target payoff date is enabled.
slider_payment = None
required_payment_preview = None


if target_payoff_date is not None:
    loan_start_date_preview = calculate_loan_start_date(
        maturity_date,
        original_term_months
    )
    current_month_preview = calculate_current_month(
        loan_start_date_preview,
        original_term_months,
        as_of_date
    )
    target_count_preview = count_payments_through_target(
        loan_start_date_preview,
        current_month_preview,
        target_payoff_date
    )
    required_payment_preview = calculate_required_payment(
        outstanding_loan_amount,
        annual_rate,
        target_count_preview
    )
    # st.metric(
    # "Recommended Payment",
    # f"${required_payment_preview:,.2f}"
    # )
    # if "payment_slider" not in st.session_state:
    #     st.session_state.payment_slider = float(
    #         round(required_payment_preview, 2)
    #     )

    # if st.button("Use Recommended Payment"):
    #     st.session_state.payment_slider = float(
    #         round(required_payment_preview, 2)
    #     )

    # st.subheader("Target Date Payment Slider")
    col1, col2 = st.columns([3, 1])

    with col1:
        st.metric(
            "Recommended Payment",
            f"${required_payment_preview:,.2f}"
        )   
    if "payment_slider" not in st.session_state:
        st.session_state.payment_slider = float(
            round(required_payment_preview, 2)
        )   
    with col2:
        if st.button("Use Recommended Payment"):
            st.session_state.payment_slider = float(
                round(required_payment_preview, 2)
                
            )

            st.rerun()   

    

    st.subheader("Target Date Payment Slider")
    st.caption("Move this slider to test whether a different monthly payment reaches the selected target payoff date.")

    min_slider = max(1.0, float(standard_payment))
    max_slider = max(
        float(required_payment_preview * 1.5),
        float(standard_payment + 1000)
        )

    slider_payment = st.slider(
            "Test Monthly Payment",
            min_value=float(round(min_slider, 2)),
            max_value=float(round(max_slider, 2)),
            # value=float(st.session_state.payment_slider),
            step=25.0,
            format="$%.2f",
            key="payment_slider"
        )
    
    st.caption(
        f"Selected Payment: ${slider_payment:,.2f}"
    )


try:
    result = run_analysis(
        original_loan_amount=original_loan_amount,
        outstanding_loan_amount=outstanding_loan_amount,
        annual_rate=annual_rate,
        standard_payment=standard_payment,
        extra_payment=extra_payment,
        maturity_date=maturity_date,
        original_term_months=original_term_months,
        as_of_date=as_of_date,
        target_payoff_date=target_payoff_date,
        slider_payment=slider_payment,
        show_full_history=show_full_history
    )

    st.subheader("Loan Position")
    loan_progress_pct = round(
        (
            (original_loan_amount - outstanding_loan_amount)
            / original_loan_amount
        ) * 100,
        1
    )
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Current Month", result["Current Month"])
    col2.metric("Months Completed", result["Months Completed"])
    col3.metric("Remaining Term", result["Remaining Term Months"])
    col4.metric("Loan Start Date", str(result["Loan Start Date"]))
    col5.metric("Loan Progress", f"{loan_progress_pct}%")
    st.subheader("Scenario Summary")

    base = result["Baseline"]
    fixed = result["Fixed Extra"]
    target = result["Target"]
    slider = result["Slider"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("### Baseline")
        st.metric("Payment", format_currency(base["Payment Amount"]))
        st.metric("Payoff Date", str(base["Payoff Date"]))
        st.metric("Remaining Interest", format_currency(base["Total Interest"]))
        st.metric("Total Remaining Paid", format_currency(base["Total Paid"]))

    # with col2:
    #     st.markdown("### Fixed Extra")
    #     st.metric("Payment", format_currency(fixed["Payment Amount"]))
    #     st.metric("Fixed Extra Payment", format_currency(fixed["Payment Amount"]))
    #     st.metric("Payoff Date", str(fixed["Payoff Date"]))
    #     st.metric("Months Saved", result["Fixed Months Saved"])
    #     st.metric("Interest Saved", format_currency(result["Fixed Interest Saved"]))
        
        
    with col2:
        st.markdown("### Fixed Extra")

        st.metric(
            "Monthly Payment",
            format_currency(fixed["Payment Amount"])
        )

        st.metric(
            "Extra Payment",
            format_currency(result["Extra Payment"])
        )

        st.metric(
            "Payoff Date",
            str(fixed["Payoff Date"])
        )

        st.metric(
            "Months Saved",
            result["Fixed Months Saved"]
        )

        st.metric(
            "Interest Saved",
            format_currency(result["Fixed Interest Saved"])
        )


    with col3:
        st.markdown("### Required Target")
        if result["Target Date Specified"]:
            st.metric("Required Payment", format_currency(result["Required Target Payment"]))
            st.metric("Required Extra", format_currency(result["Required Target Extra Payment"]))
            st.metric("Target Achieved", "YES" if result["Target Achieved"] else "NO")
            st.metric("Payoff Date", str(target["Payoff Date"]))
        else:
            st.info("No target payoff date selected.")

    with col4:
        st.markdown("### Slider Test")
        if slider is not None:
            if result["Slider Target Achieved"]:
                st.success("✅ Target Date Reached")
            else:
                st.error("❌ Target Date Missed")
            st.metric("Slider Payment", format_currency(result["Slider Payment"]))
            st.metric("Slider Extra", format_currency(result["Slider Extra Payment"]))
            # st.metric("Target Achieved", "YES" if result["Slider Target Achieved"] else "NO")
            st.metric("Target Achieved","✅ YES" if result["Slider Target Achieved"] else "❌ NO")
            st.metric("Payoff Date", str(slider["Payoff Date"]))
            st.metric("Months Saved",result["Slider Months Saved"])
            st.metric("Interest Saved", format_currency(result["Slider Interest Saved"]))
        else:
            st.info("Enable target payoff date to use slider.")

    if slider is not None:
        if result["Slider Target Achieved"]:
            st.success(
                f"Slider payment {format_currency(result['Slider Payment'])} reaches the target payoff date."
            )
        else:
            st.warning(
                f"Slider payment {format_currency(result['Slider Payment'])} does not reach the target payoff date."
            )

    df = pd.DataFrame(result["Combined Rows"])

    st.subheader("Monthly Schedule Comparison")
    st.dataframe(df, use_container_width=True)

    st.subheader("Balance Comparison")
    chart_df = df.set_index("Payment Date")[[
        "Baseline Balance",
        "Fixed Extra Balance"
    ]]

    if result["Target Date Specified"]:
        chart_df["Required Target Balance"] = df.set_index("Payment Date")["Required Target Balance"]

    if result["Slider"] is not None:
        chart_df["Slider Balance"] = df.set_index("Payment Date")["Slider Balance"]

    st.line_chart(chart_df)

    st.subheader("Principal Advance")
    advance_df = df.set_index("Payment Date")[["Fixed Extra Advance"]]

    if result["Slider"] is not None:
        advance_df["Slider Advance"] = df.set_index("Payment Date")["Slider Advance"]

    st.line_chart(advance_df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Schedule as CSV",
        data=csv,
        file_name="loan_payoff_schedule_with_slider.csv",
        mime="text/csv"
    )
    

except Exception as exc:
    st.error(str(exc))
