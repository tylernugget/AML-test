
import streamlit as st

st.set_page_config(page_title="AML Unified Loan Engine")

st.title("AML Unified Loan Engine")
st.markdown("Check loan eligibility across **AD Mortgage** and **AmWest** programs.")

st.sidebar.header("Loan Scenario Inputs")

fico = st.sidebar.number_input("FICO Score", min_value=300, max_value=850, value=700)
ltv = st.sidebar.slider("LTV (%)", min_value=0, max_value=100, value=80)
loan_amount = st.sidebar.number_input("Loan Amount", min_value=10000, step=1000, value=300000)
occupancy = st.sidebar.selectbox("Occupancy", ["primary", "second_home", "investment"])
loan_purpose = st.sidebar.selectbox("Loan Purpose", ["purchase", "rate/term", "cash_out"])
property_type = st.sidebar.selectbox("Property Type", ["SFR", "Condo", "PUD", "2-4 Unit"])
state = st.sidebar.text_input("State", value="TX")
is_first_time_homebuyer = st.sidebar.selectbox("First-Time Homebuyer?", ["Yes", "No"]) == "Yes"
unit_count = st.sidebar.number_input("Number of Units", min_value=1, max_value=4, value=1)
doc_type = st.sidebar.selectbox("Documentation Type", ["DSCR", "Full Doc"])
dscr_input = st.sidebar.text_input("DSCR (or N/A)", value="1.1")
dscr = float(dscr_input) if dscr_input.upper() != "N/A" else None

scenario = {
    "fico": fico,
    "ltv": ltv,
    "loan_amount": loan_amount,
    "occupancy": occupancy,
    "loan_purpose": loan_purpose,
    "property_type": property_type,
    "state": state,
    "is_first_time_homebuyer": is_first_time_homebuyer,
    "unit_count": unit_count,
    "doc_type": doc_type,
    "dscr": dscr
}

def check_ad_dscr_program(s):
    if s["doc_type"] != "DSCR":
        return False, "Not a DSCR doc type"
    if s["fico"] < 620:
        return False, "FICO too low for AD DSCR"
    if s["dscr"] is None or s["dscr"] < 0.75:
        return False, "DSCR too low or missing"
    if s["ltv"] > 80:
        return False, "LTV exceeds max for AD DSCR"
    return True, "Eligible for AD DSCR"

def evaluate_ad_programs(s):
    return {
        "AD - DSCR": check_ad_dscr_program(s),
    }

def check_am_va(s):
    if s["occupancy"] != "primary":
        return False, "VA requires primary occupancy"
    if s["loan_amount"] > 1000000:
        return False, "Exceeds VA max loan"
    if s["unit_count"] not in [1,2,3,4]:
        return False, "VA not allowed for that unit count"
    if s["ltv"] <= 100 and s["fico"] >= 620:
        return True, "Eligible for AmWest VA"
    return False, "FICO/LTV doesn't qualify"

def check_am_homeone(s):
    if not s["is_first_time_homebuyer"]:
        return False, "HomeOne requires first-time buyer"
    if s["ltv"] > 97 or s["fico"] < 620:
        return False, "Outside HomeOne LTV/FICO range"
    return True, "Eligible for AmWest HomeOne"

def evaluate_amwest_programs(s):
    return {
        "AmWest - VA": check_am_va(s),
        "AmWest - HomeOne": check_am_homeone(s),
    }

def evaluate_all_lenders(scenario):
    results = {}
    results.update(evaluate_ad_programs(scenario))
    results.update(evaluate_amwest_programs(scenario))
    return results

st.subheader("Results")

results = evaluate_all_lenders(scenario)

if results:
    for prog, (eligible, reason) in results.items():
        if eligible:
            st.success(f"✅ {prog}: {reason}")
        else:
            st.error(f"❌ {prog}: {reason}")
else:
    st.warning("No programs found to evaluate.")
