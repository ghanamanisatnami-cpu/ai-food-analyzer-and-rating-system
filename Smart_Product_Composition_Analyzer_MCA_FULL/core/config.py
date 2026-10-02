import os
from dotenv import load_dotenv
load_dotenv()

APP_TITLE = os.getenv("APP_TITLE", "Smart Product Composition Analyzer")
RULE_VERSION = "v1.0-demo"
CATEGORIES = ["Beverage","Snack","Cereal","Bakery","Dairy","Ready-to-eat","Other"]

TESSERACT_CMD = os.getenv("TESSERACT_CMD", "")
