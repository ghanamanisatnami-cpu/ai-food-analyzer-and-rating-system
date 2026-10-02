# Installation Guide

## Windows

1. Install Python 3.11 or later.
2. Install MySQL 8.x and create the database with `database/schema.sql`.
3. Install Tesseract OCR.
4. Open Command Prompt in the project directory.
5. Create environment:
   `python -m venv .venv`
6. Activate:
   `.venv\Scripts\activate`
7. Install:
   `pip install -r requirements.txt`
8. Copy `.env.example` to `.env`.
9. Edit `DATABASE_URL`.
10. If required, set `TESSERACT_CMD`.
11. Run:
   `streamlit run app/main.py`

## Linux

Install system packages for MySQL and Tesseract, then:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```
