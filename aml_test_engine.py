
import streamlit as st

st.title("AML Test Engine")

st.sidebar.header("Loan Scenario Inputs")

fico = st.sidebar.number_input("FICO Score", min_value=300, max_value=850, value=700)
loan_amount = st.sidebar.number_input("Loan Amount", min_value=10000, step=1000, value=230000)
property_value = st.sidebar.number_input("Property Value", min_value=10000, step=1000, value=500000)
ltv = loan_amount / property_value * 100 if property_value else 0

occupancy = st.sidebar.selectbox("Occupancy Type", ["Primary", "Second Home", "Investment"])
loan_purpose = st.sidebar.selectbox("Loan Purpose", ["Purchase", "Rate/Term Refinance", "Cash-Out Refinance"])
property_type = st.sidebar.selectbox("Property Type", ["SFR", "2-4 Unit", "Condo", "Other"])
state = st.sidebar.text_input("State (e.g., TX)", value="TX")
doc_type = st.sidebar.selectbox("Documentation Type", ["DSCR", "Bank Statement", "Full Doc", "P&L"])
dscr = st.sidebar.number_input("DSCR", min_value=0.0, step=0.01, value=1.0)
first_time_homebuyer = st.sidebar.selectbox("First-Time Homebuyer?", ["Yes", "No"])
financed_props = st.sidebar.number_input("Number of Financed Properties", min_value=0, value=1)

eligible = False
eligibility_reasons = []

if doc_type == "DSCR":
    if fico >= 680 or (fico >= 620 and dscr >= 1.0):
        if occupancy == "Investment" and property_type in ["SFR", "2-4 Unit"]:
            if ltv <= 80:
                eligible = True
            else:
                eligibility_reasons.append("LTV exceeds 80% limit.")
        else:
            eligibility_reasons.append("DSCR program is for investment properties only.")
    else:
        eligibility_reasons.append("FICO must be >= 680 if DSCR < 1.0 or >= 620 with DSCR ≥ 1.0.")

st.subheader("Results")

if eligible:
    st.success("✅ Eligible for AD Mortgage DSCR Program")
    st.markdown(f"- **FICO:** {fico}")
    st.markdown(f"- **LTV:** {ltv:.2f}%")
    st.markdown(f"- **DSCR:** {dscr}")
    st.markdown(f"- Property Type: {property_type}")
    st.markdown(f"- Purpose: {loan_purpose}")
else:
    st.error("❌ Not Eligible")
    for reason in eligibility_reasons:
        st.markdown(f"- {reason}")
