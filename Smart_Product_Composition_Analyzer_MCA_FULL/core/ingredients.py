import re

INGREDIENT_KB = {
    "sugar": ("Added/Free Sugar", "watch"),
    "glucose syrup": ("Added Sugar Syrup", "watch"),
    "fructose syrup": ("Added Sugar Syrup", "watch"),
    "hydrogenated": ("Hydrogenated Fat", "high_attention"),
    "partially hydrogenated": ("Hydrogenated Fat", "high_attention"),
    "maltodextrin": ("Refined Carbohydrate", "watch"),
    "whole grain": ("Whole Grain", "positive"),
    "whole wheat": ("Whole Grain", "positive"),
    "oats": ("Whole Grain", "positive"),
    "oat": ("Whole Grain", "positive"),
    "fibre": ("Dietary Fibre", "positive"),
    "fiber": ("Dietary Fibre", "positive"),
    "nuts": ("Nuts", "neutral"),
    "peanut": ("Nuts", "neutral"),
    "milk": ("Dairy", "neutral"),
    "salt": ("Salt", "watch"),
}

def split_ingredients(text: str):
    text = re.sub(r"^(ingredients?|composition)\s*[:\-]\s*", "", text, flags=re.I)
    return [x.strip(" .;") for x in re.split(r",|;|\n", text) if x.strip()]

def normalize_name(name: str):
    return re.sub(r"\s+", " ", re.sub(r"[^a-zA-Z0-9% .\-]", "", name)).strip().lower()

def detect_ingredients(text: str):
    items = split_ingredients(text)
    results = []
    for item in items:
        n = normalize_name(item)
        category, flag = ("Unclassified", "none")
        for key, value in INGREDIENT_KB.items():
            if key in n:
                category, flag = value
                break
        results.append({
            "ingredient_name": item,
            "normalized_name": n,
            "ingredient_category": category,
            "risk_flag": flag
        })
    return results
