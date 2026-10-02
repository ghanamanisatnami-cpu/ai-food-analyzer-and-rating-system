# Smart Product Composition Analyzer Using AI — Full MCA Project

**Course:** MCSP-232 • Master of Computer Applications  
**Basis:** supplied project synopsis

## Implemented product

This build expands the first prototype into a polished academic application structure:

1. Professional Streamlit dashboard UI
2. MySQL 8.x relational schema
3. SQLAlchemy database connection layer
4. Password hashing and role-ready authentication
5. OCR preprocessing using OpenCV
6. Tesseract OCR extraction with confidence calculation
7. Nutrition text parser
8. Ingredient splitting, normalization and knowledge-base classification
9. Rule-based AI expert system with configurable rules
10. Transparent 0–100 composition index
11. Five project-defined categories
12. Positive/negative factor explanations
13. Product comparison
14. PDF assessment reports
15. Administrator knowledge-base screen
16. Audit-log-ready schema
17. Demo seed data
18. Pytest unit tests
19. Project screenshot assets
20. MySQL schema and deployment documentation

## Run

### 1. Install prerequisites

- Python 3.11+
- MySQL 8.x
- Tesseract OCR 5.x
- Windows/Linux/macOS

### 2. Create database

Run:

```sql
SOURCE database/schema.sql;
```

### 3. Configure environment

Copy `.env.example` to `.env` and update:

```text
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/smart_product_analyzer
TESSERACT_CMD=
```

### 4. Install Python packages

```bash
pip install -r requirements.txt
```

### 5. Run

```bash
streamlit run app/main.py
```

### Demo accounts

- `admin / admin123`
- `demo / demo123`

These are development credentials only. Change them before deployment.

## OCR installation

Install Tesseract separately. On Windows, if it is not on PATH, set:

```text
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

## Test

```bash
pytest -q
```

## PDF reports

The Reports screen creates a PDF containing:
- product details
- composition index
- assessment category
- normalized nutrient values
- detected ingredients
- contributing factors
- project methodology note

## Database architecture

The schema follows the synopsis entities:
users → products → compositions → nutrients / ingredients → analyses → analysis_factors → explanations, plus knowledge_rules and audit_logs.

The implementation keeps MySQL as the intended deployment database. The UI also contains a self-contained demo mode so the interface can be demonstrated without a live database connection; final deployment should wire all persistence to MySQL.

## Academic integrity / scoring note

The supplied synopsis defines:

Score = clamp(50 + sum of triggered rule weights, 0, 100); positive weights increase the score and negative weights decrease it.

and category ranges:
0–19 Very Low, 20–39 Low, 40–59 Moderate, 60–79 Good, 80–100 High.

The nutrient thresholds and weights in `core/rules.py` are explicitly marked as demo implementation values. The final MCA report should replace them with the actual documented knowledge-base values and source/version that were used during development and testing.

The application is informational. It does not diagnose disease, provide individualized clinical nutrition advice, certify regulatory compliance, or guarantee food safety.

## Suggested final project evidence

For the final report, capture screenshots of:
1. Login
2. Dashboard
3. Product entry
4. OCR preview
5. Nutrition composition form
6. Assessment result
7. Ingredient detection
8. History
9. Comparison
10. PDF report
11. Admin knowledge base
12. Database tables / MySQL Workbench

The included screenshots are labeled as **prototype UI screenshots** unless captured from a running environment.

## Synopsis traceability

The project directly follows the synopsis workflow:
Login → product → label/manual composition → OCR → parse/normalize → validate → features → knowledge rules → score/category → factors → save → display/report.

See the supplied synopsis for the formal MCSP-232 requirements and project boundary.
