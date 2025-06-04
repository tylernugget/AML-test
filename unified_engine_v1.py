
# Unified Loan Product Eligibility Engine (AD Mortgage + AmWest)

# Sample scenario input
scenario = {
    "fico": 700,
    "ltv": 80,
    "loan_amount": 300000,
    "occupancy": "investment",
    "loan_purpose": "purchase",
    "property_type": "SFR",
    "state": "TX",
    "is_first_time_homebuyer": False,
    "unit_count": 1,
    "dscr": 1.1,
    "doc_type": "DSCR"
}

### AD MORTGAGE LOGIC ###

def check_ad_dscr_program(s):
    if s["doc_type"] != "DSCR":
        return False, "Not a DSCR doc type"
    if s["fico"] < 620:
        return False, "FICO too low for AD DSCR"
    if s["dscr"] < 0.75:
        return False, "DSCR too low for AD DSCR minimum"
    if s["ltv"] > 80:
        return False, "LTV exceeds max for AD DSCR"
    return True, "Eligible for AD DSCR"

def evaluate_ad_programs(s):
    return {
        "AD - DSCR": check_ad_dscr_program(s),
        # Add more AD Mortgage program evaluations here...
    }

### AMWEST LOGIC ###

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
        # Add more AmWest program evaluations here...
    }

### COMBINED EVALUATOR ###

def evaluate_all_lenders(scenario):
    results = {}
    results.update(evaluate_ad_programs(scenario))
    results.update(evaluate_amwest_programs(scenario))
    return results

# Run it
results = evaluate_all_lenders(scenario)

# Show breakdown
print("\n--- LOAN PROGRAM ELIGIBILITY ---\n")
for prog, (eligible, reason) in results.items():
    status = "✅ Eligible" if eligible else "❌ Ineligible"
    print(f"{status} - {prog}: {reason}")
