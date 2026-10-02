RULES = [
    {"name":"Total sugars", "field":"sugars", "operator":">", "threshold":10.0, "weight":-2.0, "unit":"g/100g",
     "source_ref":"Project knowledge-base; replace with final documented reference"},
    {"name":"Saturated fat", "field":"sat_fat", "operator":">", "threshold":5.0, "weight":-2.0, "unit":"g/100g",
     "source_ref":"Project knowledge-base; replace with final documented reference"},
    {"name":"Trans fat", "field":"trans_fat", "operator":">", "threshold":0.5, "weight":-5.0, "unit":"g/100g",
     "source_ref":"Project knowledge-base; replace with final documented reference"},
    {"name":"Sodium", "field":"sodium", "operator":">", "threshold":400.0, "weight":-1.5, "unit":"mg/100g",
     "source_ref":"Project knowledge-base; replace with final documented reference"},
    {"name":"Protein", "field":"protein", "operator":">=", "threshold":5.0, "weight":1.5, "unit":"g/100g",
     "source_ref":"Project knowledge-base; replace with final documented reference"},
    {"name":"Dietary fibre", "field":"fibre", "operator":">=", "threshold":3.0, "weight":1.5, "unit":"g/100g",
     "source_ref":"Project knowledge-base; replace with final documented reference"},
]

def category(score):
    if score < 20: return "Very Low"
    if score < 40: return "Low"
    if score < 60: return "Moderate"
    if score < 80: return "Good"
    return "High"

def calculate(values, ingredient_results=None):
    score = 50.0
    factors = []
    missing = []
    for rule in RULES:
        value = values.get(rule["field"])
        if value is None:
            missing.append(rule["field"])
            continue
        triggered = (value > rule["threshold"] if rule["operator"] == ">"
                     else value >= rule["threshold"])
        if triggered:
            score += rule["weight"]
            factors.append({**rule, "value": value, "contribution": rule["weight"]})
    # Ingredient flags are explanatory only in this baseline implementation.
    if ingredient_results:
        for x in ingredient_results:
            if x["risk_flag"] == "high_attention":
                factors.append({
                    "name": f"Ingredient flag: {x['ingredient_name']}",
                    "field": "ingredient",
                    "value": None,
                    "threshold": None,
                    "weight": 0,
                    "unit": "",
                    "source_ref": "Ingredient-category knowledge base",
                    "contribution": 0
                })
    score = max(0.0, min(100.0, score))
    return round(score, 2), category(score), factors, missing
