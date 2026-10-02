import re
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import pytesseract

def configure_tesseract(cmd: str | None = None):
    if cmd:
        pytesseract.pytesseract.tesseract_cmd = cmd

def preprocess_image(file_bytes: bytes):
    arr = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Unable to decode image.")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=1.6, fy=1.6, interpolation=cv2.INTER_CUBIC)
    denoise = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    threshold = cv2.adaptiveThreshold(
        denoise, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 11
    )
    return image, threshold

def extract_text(file_bytes: bytes):
    original, processed = preprocess_image(file_bytes)
    config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(processed, config=config)
    data = pytesseract.image_to_data(processed, config=config, output_type=pytesseract.Output.DICT)
    conf = [float(x) for x in data["conf"] if str(x).strip() not in ("", "-1")]
    confidence = round(sum(conf) / len(conf), 1) if conf else 0.0
    return original, processed, text, confidence

def parse_nutrition(text: str):
    patterns = {
        "energy": r"(?:energy|calor(?:y|ies)).{0,30}?(\d+(?:\.\d+)?)\s*k?cal",
        "carbs": r"(?:total\s+)?carbohydrate.{0,30}?(\d+(?:\.\d+)?)\s*g",
        "sugars": r"(?:total\s+)?sugars?.{0,30}?(\d+(?:\.\d+)?)\s*g",
        "added_sugar": r"added\s+sugars?.{0,30}?(\d+(?:\.\d+)?)\s*g",
        "protein": r"protein.{0,30}?(\d+(?:\.\d+)?)\s*g",
        "fat": r"(?:total\s+)?fat.{0,30}?(\d+(?:\.\d+)?)\s*g",
        "sat_fat": r"(?:saturated|sat\.?)\s*fat.{0,30}?(\d+(?:\.\d+)?)\s*g",
        "trans_fat": r"trans\s*fat.{0,30}?(\d+(?:\.\d+)?)\s*g",
        "fibre": r"(?:dietary\s*)?fibr[ea].{0,30}?(\d+(?:\.\d+)?)\s*g",
        "sodium": r"sodium.{0,30}?(\d+(?:\.\d+)?)\s*mg",
    }
    result = {}
    for field, pattern in patterns.items():
        m = re.search(pattern, text, flags=re.I | re.S)
        if m:
            result[field] = float(m.group(1))
    return result
