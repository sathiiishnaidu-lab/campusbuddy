st.markdown("""
<style>
/* Premium CampusBuddy AI theme */
.stApp {
    background:
        radial-gradient(ellipse at top left, rgba(124,58,237,.20), transparent 42%),
        radial-gradient(ellipse at top right, rgba(59,130,246,.12), transparent 35%),
        #09090f;
    color: #f5f3ff;
}

[data-testid="stSidebar"] {
    background: #0e0d16;
    border-right: 1px solid rgba(167,139,250,.18);
}

h1, h2, h3 {
    color: #f5f3ff !important;
    letter-spacing: -0.6px;
}

.stButton > button {
    background: linear-gradient(135deg, #8b5cf6, #6366f1);
    color: white;
    border: 1px solid rgba(196,181,253,.25);
    border-radius: 12px;
    font-weight: 600;
    transition: .2s ease;
}

.stButton > button:hover {
    border-color: #c4b5fd;
    box-shadow: 0 0 20px rgba(139,92,246,.3);
    transform: translateY(-1px);
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #191625, #101019);
    border: 1px solid rgba(167,139,250,.2);
    border-radius: 16px;
    padding: 16px;
}

[data-testid="stChatMessage"] {
    background: rgba(25,24,40,.75);
    border: 1px solid rgba(167,139,250,.15);
    border-radius: 16px;
}

.stTextInput input, .stTextArea textarea {
    background: #13121d;
    color: white;
    border: 1px solid #39334f;
    border-radius: 12px;
}

hr {
    border-color: rgba(167,139,250,.2);
}

.small-muted {
    color: #9690b1;
    font-size: 12px;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)