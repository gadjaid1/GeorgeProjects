# Enhanced Loan Payoff Analysis - Streamlit App with Payment Slider

## Run locally

```bash
cd LoanApp
pip install -r requirements.txt
streamlit run EnhancedLoanPayoffAnalysis_Streamlit_slider.py
```

## New feature

This version adds a target-date payment slider. When a target payoff date is enabled, the app calculates the required payment and then lets you move a slider to test other monthly payment amounts.

The app tells you whether the slider-selected payment reaches the target payoff date.

## Features

- Baseline payoff without extra payment
- Fixed extra payment scenario
- Required target payoff scenario
- Payment slider for target date testing
- Required monthly payment to reach target date
- Required extra payment above regular payment
- Months saved
- Interest saved
- Balance comparison charts
- Principal advance chart
- CSV download
