# Test Plan

| ID | Test | Expected |
|---|---|---|
| T01 | Valid login | Dashboard opens |
| T02 | Invalid login | Access denied |
| T03 | Product without name | Validation error |
| T04 | Valid nutrition input | Analysis completes |
| T05 | High sugar input | Negative sugar factor |
| T06 | Protein/fibre threshold | Positive factors |
| T07 | Score lower bound | Never below 0 |
| T08 | Score upper bound | Never above 100 |
| T09 | Ingredient splitting | Individual entries detected |
| T10 | Ingredient classification | Known ingredient category |
| T11 | OCR parser | Numeric values extracted |
| T12 | OCR failure | Error displayed without crash |
| T13 | History | Saved analyses displayed |
| T14 | Comparison | Selected products displayed |
| T15 | PDF report | Downloadable PDF created |
| T16 | Admin | Knowledge base visible to admin |
| T17 | Non-admin admin page | Access denied |
