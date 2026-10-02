from core.ocr import parse_nutrition

def test_nutrition_parser():
    text = """
    Energy 450 kcal
    Total Carbohydrate 60 g
    Total Sugars 18 g
    Protein 7 g
    Total Fat 16 g
    Saturated Fat 6 g
    Trans Fat 0.2 g
    Dietary Fibre 4 g
    Sodium 520 mg
    """
    x = parse_nutrition(text)
    assert x["energy"] == 450
    assert x["sugars"] == 18
    assert x["sodium"] == 520
