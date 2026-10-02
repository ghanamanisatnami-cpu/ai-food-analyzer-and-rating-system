from core.ingredients import detect_ingredients

def test_ingredient_detection():
    result = detect_ingredients("Whole wheat flour, sugar, partially hydrogenated vegetable oil, salt")
    assert len(result) == 4
    assert any(x["ingredient_category"] == "Whole Grain" for x in result)
    assert any(x["risk_flag"] == "high_attention" for x in result)
