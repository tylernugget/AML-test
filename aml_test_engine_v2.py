
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
doc_type = st.sidebar.selectbox("Documentation Type", ["DSCR", "Bank Statement", "Full Doc", "P&L", "Asset Utilization"])

dscr_input = st.sidebar.text_input("DSCR (Enter 'N/A' if not applicable)", value="1.0")
try:
    dscr = float(dscr_input) if dscr_input.upper() != "N/A" else None
except ValueError:
    dscr = None

first_time_homebuyer = st.sidebar.selectbox("First-Time Homebuyer?", ["Yes", "No"])
financed_props = st.sidebar.number_input("Number of Financed Properties", min_value=0, value=1)

eligible = False
program_name = ""
eligibility_reasons = []

# Begin logic for AD Mortgage products
if doc_type == "DSCR":
    if dscr is None:
        eligibility_reasons.append("DSCR value required for DSCR loans.")
    else:
        if fico >= 680 or (fico >= 620 and dscr >= 1.0):
            if occupancy == "Investment" and property_type in ["SFR", "2-4 Unit"]:
                if ltv <= 80:
                    eligible = True
                    program_name = "AD Mortgage DSCR Program"
                else:
                    eligibility_reasons.append("LTV exceeds 80% limit.")
            else:
                eligibility_reasons.append("DSCR program is for investment properties only.")
        else:
            eligibility_reasons.append("FICO must be ≥ 680 if DSCR < 1.0 or ≥ 620 with DSCR ≥ 1.0.")

elif doc_type == "Full Doc":
    if fico >= 620:
        if occupancy in ["Primary", "Second Home"]:
            if ltv <= 95:
                eligible = True
                program_name = "AD Mortgage Full Doc (Prime / Agency)"
            else:
                eligibility_reasons.append("LTV too high for Full Doc.")
        elif occupancy == "Investment":
            if ltv <= 85:
                eligible = True
                program_name = "AD Mortgage Full Doc Investment"
            else:
                eligibility_reasons.append("Investment Full Doc LTV exceeds 85% limit.")
        else:
            eligibility_reasons.append("Invalid occupancy for Full Doc.")
    else:
        eligibility_reasons.append("FICO too low for Full Doc.")

elif doc_type == "Bank Statement":
    if fico >= 620 and occupancy in ["Primary", "Investment"]:
        if ltv <= 90:
            eligible = True
            program_name = "AD Mortgage Bank Statement Program"
        else:
            eligibility_reasons.append("LTV too high for Bank Statement.")
    else:
        eligibility_reasons.append("Bank Statement program FICO or occupancy issue.")

elif doc_type == "P&L":
    if fico >= 620 and occupancy in ["Primary", "Investment"]:
        if ltv <= 80:
            eligible = True
            program_name = "AD Mortgage P&L Program"
        else:
            eligibility_reasons.append("LTV too high for P&L.")
    else:
        eligibility_reasons.append("P&L FICO or occupancy issue.")

elif doc_type == "Asset Utilization":
    if fico >= 680 and occupancy in ["Primary", "Second Home"]:
        if ltv <= 75:
            eligible = True
            program_name = "AD Mortgage Asset Utilization"
        else:
            eligibility_reasons.append("LTV too high for Asset Utilization.")
    else:
        eligibility_reasons.append("Asset Utilization requires FICO ≥ 680 and Primary/2nd occupancy.")

# Output Results
st.subheader("Results")

if eligible:
    st.success(f"✅ Eligible for {program_name}")
    st.markdown(f"- **FICO:** {fico}")
    st.markdown(f"- **LTV:** {ltv:.2f}%")
    st.markdown(f"- **Documentation:** {doc_type}")
    if dscr_input.upper() != "N/A":
        st.markdown(f"- **DSCR:** {dscr}")
    st.markdown(f"- **Occupancy:** {occupancy}")
    st.markdown(f"- **Loan Purpose:** {loan_purpose}")
else:
    st.error("❌ Not Eligible")
    for reason in eligibility_reasons:
        st.markdown(f"- {reason}")
