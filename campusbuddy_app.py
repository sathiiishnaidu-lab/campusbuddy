import json
import requests
import streamlit as st
from datetime import datetime

# ============================================================
# CampusBuddy AI — single-file Streamlit app
# Local AI: Ollama + Gemma
# Add campus-specific facts only after verifying official sources.
# ============================================================

st.set_page_config(
    page_title="CampusBuddy AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"

# Fill these fields with information confirmed by an official campus source.
# Leave unknown fields blank: the assistant will say they are not verified.
CAMPUS_FACTS = {
    "college_name": "NIAT / Lingaya's campus (confirm the official display name)",
    "official_address": "",
    "official_website": "",
    "class_timings": "",
    "office_hours": "",
    "academic_calendar_url": "",
    "verified_source_url": "",
}

DEFAULT_EVENTS = [
    {
        "name": "Sample Tech Talk",
        "date": "Add confirmed date",
        "place": "Add confirmed venue",
        "details": "DEMO EVENT — replace this with an official announcement.",
    },
    {
        "name": "Sample Coding Meetup",
        "date": "Add confirmed date",
        "place": "Add confirmed venue",
        "details": "DEMO EVENT — replace this with an official announcement.",
    },
]

FAQS = [
    ("How can I confirm class timings?", "Check your latest timetable or an official college notice. If verified timings have not been added to CampusBuddy, it will tell you that the information is unavailable."),
    ("Where can I find the campus address?", "Use the address listed in the official college website or the verified campus information entered by the administrator."),
    ("How do I report a lost item?", "Open Lost & Found, provide a description and a safe contact method, then submit the report."),
    ("Can I make a practice quiz?", "Yes. Open Quiz Maker, enter a topic and choose the number of questions. Review AI-generated questions before using them in a real assessment."),
]

# ------------------ Visual theme ------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
.stApp {
  background:
    radial-gradient(ellipse at 15% 0%, rgba(104,65,210,.22), transparent 36%),
    radial-gradient(ellipse at 90% 10%, rgba(39,116,190,.12), transparent 30%),
    #090b14;
  color: #f4f2ff;
  font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: rgba(9,11,20,.78); }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1450px; }
h1,h2,h3 { font-family: 'Space Grotesk', sans-serif; letter-spacing: -.03em; }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#131226 0%,#0d1020 100%);
  border-right: 1px solid rgba(173,151,255,.19);
  min-width: 285px;
}
[data-testid="stSidebar"] .block-container { padding-top: 1.4rem; }
[data-testid="stSidebar"] [data-testid="stRadio"] > div { gap: 8px; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  background: rgba(255,255,255,.035);
  border: 1px solid rgba(255,255,255,.07);
  padding: 11px 13px;
  border-radius: 13px;
  transition: all .18s ease;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(139,92,246,.16);
  border-color: rgba(167,139,250,.4);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p { font-weight: 600; font-size: 1rem; }
.hero {
  padding: 28px 30px; border-radius: 24px;
  background: linear-gradient(120deg,rgba(113,74,224,.23),rgba(34,52,94,.22));
  border: 1px solid rgba(177,157,255,.22);
  box-shadow: 0 18px 55px rgba(0,0,0,.18); margin-bottom: 22px;
}
.eyebrow { color:#b6a4ff; font-size:.78rem; font-weight:700; letter-spacing:.15em; text-transform:uppercase; }