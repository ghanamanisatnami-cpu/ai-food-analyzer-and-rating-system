import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    .stApp { background: #f5f7fb; }
    [data-testid="stSidebar"] { background: #12263a; }
    [data-testid="stSidebar"] * { color: #eef5fb !important; }
    .hero { padding: 22px 26px; border-radius: 18px; background: linear-gradient(135deg,#123B5D,#256D85);
            color:white; margin-bottom:20px; }
    .hero h1 { margin:0; font-size:31px; }
    .hero p { margin:6px 0 0; opacity:.9; }
    .card { background:white; border-radius:16px; padding:18px; box-shadow:0 3px 16px rgba(20,40,70,.08); }
    .metric { font-size:31px; font-weight:700; }
    .muted { color:#667085; font-size:13px; }
    .tag { display:inline-block; padding:4px 10px; border-radius:20px; background:#e8f1f8; margin-right:4px; }
    </style>
    """, unsafe_allow_html=True)

def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def metric_card(label, value, note=""):
    st.markdown(f'<div class="card"><div class="muted">{label}</div><div class="metric">{value}</div><div class="muted">{note}</div></div>', unsafe_allow_html=True)
