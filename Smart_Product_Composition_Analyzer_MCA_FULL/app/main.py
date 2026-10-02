import os, json
from datetime import datetime
import streamlit as st
import pandas as pd

from core.config import APP_TITLE, CATEGORIES, TESSERACT_CMD
from core.security import hash_password, verify_password
from core.ocr import extract_text, parse_nutrition, configure_tesseract
from core.ingredients import detect_ingredients
from core.rules import calculate, RULES
from reports.pdf_report import build_report
from app.ui import inject_css, hero, metric_card

configure_tesseract(TESSERACT_CMD)

# This reference implementation keeps the UI complete. Replace repository calls
# with SQLAlchemy CRUD in the deployment environment using database/connection.py.

DEMO_USERS = {
    "admin": {"password": hash_password("admin123"), "role":"admin"},
    "demo": {"password": hash_password("demo123"), "role":"user"},
}

if "analyses" not in st.session_state:
    st.session_state.analyses = []

def login():
    inject_css()
    st.markdown('<div style="height:50px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero"><h1>🥗 Smart Product Composition Analyzer</h1><p>MCSP-232 • AI • OCR • Expert System • RDBMS</p></div>', unsafe_allow_html=True)
    with st.form("login"):
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", type="password", value="admin123")
        if st.form_submit_button("Sign in", use_container_width=True):
            u = DEMO_USERS.get(username)
            if u and verify_password(password, u["password"]):
                st.session_state.user = {"username":username, "role":u["role"]}
                st.rerun()
            st.error("Invalid username or password.")

def sidebar():
    with st.sidebar:
        st.markdown("## 🥗 SPCA")
        st.caption("Smart Product Composition Analyzer")
        page = st.radio("Workspace", ["Dashboard","Analyze Product","History","Compare","Reports","Admin"])
        st.divider()
        st.write(f"**User:** {st.session_state.user['username']}")
        st.write(f"**Role:** {st.session_state.user['role']}")
        if st.button("Logout"):
            st.session_state.clear(); st.rerun()
    return page

def dashboard():
    hero("Smart Product Composition Analyzer", "Transparent product composition analysis powered by OCR and a configurable expert system.")
    analyses = st.session_state.analyses
    c = st.columns(4)
    c[0].metric("Analyses", len(analyses))
    c[1].metric("Products", len({x["name"] for x in analyses}))
    c[2].metric("Average Index", f"{sum(x['score'] for x in analyses)/len(analyses):.1f}" if analyses else "—")
    c[3].metric("Rules", len(RULES))
    st.subheader("System workflow")
    st.markdown("**Input → OCR / Manual Entry → Parse → Normalize → Expert Rules → Weighted Score → Explanation → Report**")
    if analyses:
        st.subheader("Recent analyses")
        st.dataframe(pd.DataFrame(analyses).sort_values("created_at", ascending=False), use_container_width=True)
    else:
        st.info("Start with **Analyze Product** to create the first analysis.")

def analyze_page():
    hero("Analyze Product", "Upload a label or enter composition data manually. OCR results are reviewed before scoring.")
    left,right = st.columns([1,1])
    with left:
        name = st.text_input("Product name *")
        brand = st.text_input("Brand")
        cat = st.selectbox("Product category", CATEGORIES)
        ingredients = st.text_area("Ingredient list", height=130)
        image = st.file_uploader("Label image", type=["png","jpg","jpeg","webp"])
    ocr_text = ""
    ocr_conf = 0.0
    detected = {}
    if image:
        raw = image.getvalue()
        if st.button("Run OCR", type="secondary"):
            try:
                original, processed, ocr_text, ocr_conf = extract_text(raw)
                st.session_state.ocr_text = ocr_text
                st.session_state.ocr_conf = ocr_conf
                st.session_state.ocr_values = parse_nutrition(ocr_text)
                st.session_state.ocr_image = processed
            except Exception as e:
                st.error(f"OCR failed: {e}")
        if st.session_state.get("ocr_text"):
            with right:
                st.image(st.session_state.get("ocr_image"), caption=f"Preprocessed image • OCR confidence {st.session_state.get('ocr_conf',0)}%")
                st.text_area("OCR preview", st.session_state["ocr_text"], height=200)
            detected = st.session_state.get("ocr_values", {})
    elif st.session_state.get("ocr_values"):
        detected = st.session_state["ocr_values"]

    st.subheader("Nutrition panel — normalized basis")
    labels = [
        ("energy","Energy (kcal/100g)"),("carbs","Carbohydrate (g/100g)"),
        ("sugars","Total sugars (g/100g)"),("added_sugar","Added sugar (g/100g)"),
        ("protein","Protein (g/100g)"),("fat","Total fat (g/100g)"),
        ("sat_fat","Saturated fat (g/100g)"),("trans_fat","Trans fat (g/100g)"),
        ("fibre","Dietary fibre (g/100g)"),("sodium","Sodium (mg/100g)")
    ]
    vals={}
    cols=st.columns(3)
    for i,(key,label) in enumerate(labels):
        with cols[i%3]:
            vals[key]=st.number_input(label, min_value=0.0, value=float(detected.get(key,0.0)), step=0.1)
    if st.button("Analyze & Save", type="primary", use_container_width=True):
        if not name.strip():
            st.error("Product name is required.")
            return
        ing = detect_ingredients(ingredients)
        score, hcat, factors, missing = calculate(vals, ing)
        record={"name":name,"brand":brand,"category":cat,"score":score,"assessment":hcat,
                "created_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ingredients":ing,"values":vals,"factors":factors,"missing":missing}
        st.session_state.analyses.append(record)
        st.session_state.last = record
        st.success("Analysis completed and saved.")
    if "last" in st.session_state:
        show_result(st.session_state.last)

def show_result(r):
    st.divider()
    st.subheader("Assessment Result")
    c=st.columns(3)
    c[0].metric("Composition Index", f"{r['score']}/100")
    c[1].metric("Category", r["assessment"])
    c[2].metric("OCR / Input", "Reviewed")
    st.progress(r["score"]/100)
    p,n=st.columns(2)
    with p:
        st.markdown("### Positive / supporting factors")
        for f in r["factors"]:
            if f.get("contribution",0)>0: st.success(f"{f['name']}: +{f['contribution']}")
        if not any(f.get("contribution",0)>0 for f in r["factors"]): st.write("None triggered.")
    with n:
        st.markdown("### Attention factors")
        for f in r["factors"]:
            if f.get("contribution",0)<0: st.warning(f"{f['name']}: {f['value']} → {f['contribution']}")
            if f.get("field")=="ingredient": st.info(f"Ingredient flag: {f['name']}")
        if not any(f.get("contribution",0)<0 or f.get("field")=="ingredient" for f in r["factors"]): st.write("None triggered.")
    if r["missing"]: st.info("Missing/unsupplied analytical fields: " + ", ".join(r["missing"]))
    st.caption("Informational composition index only. It is not a medical diagnosis, personalized dietary recommendation, regulatory certification, or guarantee of food safety.")

def history_page():
    hero("Analysis History","Review previously saved analyses in the current application session.")
    if st.session_state.analyses:
        df=pd.DataFrame([{k:v for k,v in x.items() if k not in ("ingredients","values","factors","missing")} for x in st.session_state.analyses])
        st.dataframe(df,use_container_width=True)
        st.download_button("Export CSV",df.to_csv(index=False).encode(),"analysis_history.csv","text/csv")
    else: st.info("No analyses yet.")

def compare_page():
    hero("Product Comparison","Compare saved analyses on the same normalized composition basis.")
    a=st.session_state.analyses
    if len(a)<2: st.info("Create at least two analyses."); return
    names=[f"{i}: {x['name']}" for i,x in enumerate(a)]
    chosen=st.multiselect("Select products",names,default=names[:2])
    rows=[]
    for label in chosen:
        x=a[int(label.split(":")[0])]
        rows.append({"Product":x["name"],"Index":x["score"],"Category":x["assessment"],
                     "Sugar":x["values"]["sugars"],"Sat. fat":x["values"]["sat_fat"],
                     "Sodium":x["values"]["sodium"],"Protein":x["values"]["protein"],"Fibre":x["values"]["fibre"]})
    if rows: st.dataframe(pd.DataFrame(rows),use_container_width=True)

def reports_page():
    hero("Reports","Generate a formal PDF assessment for the latest analysis.")
    r=st.session_state.get("last")
    if not r: st.info("Run an analysis first."); return
    pdf=build_report(r,r["values"],r["ingredients"],r["score"],r["assessment"],r["factors"],r["created_at"])
    st.download_button("Download PDF Report",pdf,f"{r['name'].replace(' ','_')}_assessment.pdf","application/pdf",use_container_width=True)
    st.success("PDF report is ready.")

def admin_page():
    hero("Administration","Knowledge-base and system administration panel.")
    if st.session_state.user["role"]!="admin":
        st.error("Administrator role required."); return
    st.subheader("Knowledge-base rules")
    df=pd.DataFrame(RULES)
    st.dataframe(df,use_container_width=True)
    st.warning("Demo thresholds/weights are placeholders for implementation. Replace with the final documented source/version before formal submission.")
    st.subheader("Demo accounts")
    st.code("admin / admin123\ndemo / demo123")

def main():
    if "user" not in st.session_state:
        login(); return
    inject_css()
    page=sidebar()
    {"Dashboard":dashboard,"Analyze Product":analyze_page,"History":history_page,
     "Compare":compare_page,"Reports":reports_page,"Admin":admin_page}[page]()

if __name__=="__main__":
    main()
