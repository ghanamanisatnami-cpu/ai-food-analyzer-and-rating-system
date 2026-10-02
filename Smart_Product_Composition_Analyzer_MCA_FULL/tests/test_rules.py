from core.rules import calculate, category

def test_category_bands():
    assert category(10) == "Very Low"
    assert category(30) == "Low"
    assert category(50) == "Moderate"
    assert category(70) == "Good"
    assert category(90) == "High"

def test_rule_score_is_clamped():
    values = {"sugars": 100, "sat_fat": 100, "trans_fat": 100, "sodium": 10000,
              "protein": 0, "fibre": 0}
    score, _, _, _ = calculate(values)
    assert 0 <= score <= 100

def test_positive_rules():
    values = {"protein": 10, "fibre": 10}
    score, label, factors, missing = calculate(values)
    assert score > 50
    assert label in {"Moderate","Good","High"}
    assert any(f["name"] == "Protein" for f in factors)
