
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="CampusBuddy AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CYBERPUNK THEME ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at top left, #18224b 0%, transparent 42%),
        radial-gradient(ellipse at bottom right, #351342 0%, transparent 38%),
        #080b14;
    color: #edf2ff;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101528, #160e24);
    border-right: 1px solid #34345c;
}
h1, h2, h3 {
    color: #f4f5ff !important;
}
p, label, .stMarkdown {
    color: #d2d9f5;
}
div[data-testid="stMetric"] {
    background: rgba(20, 27, 52, 0.85);
    border: 1px solid #393c70;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0 0 16px rgba(91, 76, 255, 0.10);
}
.stButton > button {
    background: linear-gradient(90deg, #6755ff, #a13bff);
    color: white;
    border: 1px solid #8b7bff;
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
}
.stButton > button:hover {
    border-color: #49f5ff;
    color: #ffffff;
    box-shadow: 0 0 16px rgba(73, 245, 255, 0.25);
}
.stTextInput input, .stTextArea textarea {
    background: #11172a;
    color: white;
    border: 1px solid #414574;
    border-radius: 10px;
}
div[data-baseweb="select"] > div {
    background: #11172a;
    border-color: #414574;
}
div[data-testid="stExpander"] {
    border: 1px solid #35385f;
    border-radius: 12px;
    background: rgba(18, 22, 42, 0.75);
}
.neon-hero {
    padding: 30px;
    border: 1px solid #4b4ce5;
    border-radius: 20px;
    background: linear-gradient(120deg, rgba(72,67,180,.25), rgba(25,215,232,.08));
    box-shadow: 0 0 24px rgba(105, 75, 255, .13);
    margin-bottom: 24px;
}
.neon-tag {
    color: #57f3ff;
    letter-spacing: 3px;
    font-size: 12px;
    font-weight: 800;
}
.small-muted {
    color: #9da9d2;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION DATA ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "reports" not in st.session_state:
    st.session_state.reports = []

if "events" not in st.session_state:
    st.session_state.events = [
        {
            "name": "Campus Hackathon",
            "category": "Technology",
            "date": "Demo date — confirm with your college",
            "description": "Build a prototype, collaborate with a team, and present your solution."
        },
        {
            "name": "Coding Practice Meetup",
            "category": "Learning",
            "date": "Sample event",
            "description": "Practice beginner coding problems and learn with fellow students."
        },
        {
            "name": "Student Talent Day",
            "category": "Culture",
            "date": "Sample event",
            "description": "A sample showcase for music, art, creativity, and student projects."
        }
    ]

# ---------- AI CONNECTION ----------
def ask_ai(prompt):
    model = st.session_state.get("model", "gemma3:1b")
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "The model returned an empty response.")
    except requests.exceptions.ConnectionError:
        return (
            "I can't connect to Ollama right now. "
            "Please open Ollama and make sure it is running."
        )
    except requests.exceptions.Timeout:
        return "The model took too long to respond. Please try again."
    except Exception as error:
        return f"Something went wrong: {error}"

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🎓 CampusBuddy")
    st.markdown('<p class="neon-tag">AI CAMPUS COMPANION</p>',
                unsafe_allow_html=True)
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "🤖 AI Assistant",
            "📢 Notice Intelligence",
            "📅 Campus Events",
            "🔎 Lost & Found",
            "❓ Campus FAQs"
        ]
    )

    st.divider()
    st.markdown("### ⚙️ AI Settings")
    st.session_state.model = st.text_input(
        "Ollama model",
        value=st.session_state.get("model", "gemma3:1b")
    )
    st.caption("Local AI • Ollama • No API key")

    if st.button("🧹 Clear chat history"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        '<p class="small-muted">Student-built prototype • Demo data</p>',
        unsafe_allow_html=True
    )

# ---------- TOP HEADER ----------
st.markdown(
    '<p class="neon-tag">YOUR CAMPUS. YOUR COMMUNITY. YOUR AI.</p>',
    unsafe_allow_html=True
)

# ---------- DASHBOARD ----------
if page == "🏠 Dashboard":
    st.markdown("""
    <div class="neon-hero">
        <h1>Welcome to CampusBuddy AI ✨</h1>
        <p>Your intelligent companion for campus life, notices,
        student questions, and community connections.</p>
        <p class="small-muted">POWERED BY LOCAL OPEN-SOURCE AI</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("AI Model", st.session_state.model)
    col2.metric("Campus Events", len(st.session_state.events))
    col3.metric("Lost & Found Reports", len(st.session_state.reports))

    st.markdown("## ⚡ Explore your campus")
    st.write("Choose a module from the sidebar to get started.")

    a, b = st.columns(2)
    with a:
        st.markdown("### 🤖 AI Assistant")
        st.write("Ask questions and get helpful, beginner-friendly answers.")
        st.markdown("### 📢 Notice Intelligence")
        st.write("Extract deadlines, important dates, and action items.")
        st.markdown("### ❓ Campus FAQs")
        st.write("Find quick answers to common student questions.")
    with b:
        st.markdown("### 📅 Campus Events")
        st.write("Browse sample student events and activities.")
        st.markdown("### 🔎 Lost & Found")
        st.write("Create and browse demo reports for missing items.")

    st.info(
        "Prototype notice: event details are sample data. "
        "Confirm real dates and college information with official sources."
    )

# ---------- AI ASSISTANT ----------
elif page == "🤖 AI Assistant":
    st.markdown("## 🤖 CampusBuddy AI Assistant")
    st.write("Ask about studying, coding, teamwork, projects, or campus life.")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask CampusBuddy anything...")

    if question:
        st.session_state.chat_history.append(
            {"role": "user", "content": question}
        )
        with st.chat_message("user"):
            st.markdown(question)

        history_text = "\n".join(
            f'{m["role"]}: {m["content"]}'
            for m in st.session_state.chat_history[-8:]
        )

        prompt = f"""
You are CampusBuddy, a friendly and responsible college assistant.
Help students with clear, practical, beginner-friendly answers.
Use headings or bullet points when useful.
Never invent official campus rules, event dates, fees, or announcements.
If a college-specific fact is unknown, clearly say it needs verification.
Keep the answer focused on the student's question.

Conversation:
{history_text}

Assistant:
"""
        with st.chat_message("assistant"):
            with st.spinner("CampusBuddy is thinking..."):
                answer = ask_ai(prompt)
                st.markdown(answer)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )

# ---------- NOTICE SUMMARIZER ----------
elif page == "📢 Notice Intelligence":
    st.markdown("## 📢 Notice Intelligence")
    st.write("Turn a long notice into a clear student action plan.")

    notice = st.text_area(
        "Paste the full notice",
        height=240,
        placeholder="Paste your college announcement or notice here..."
    )

    if st.button("✨ Analyse Notice", use_container_width=True):
        if not notice.strip():
            st.warning("Please paste a notice first.")
        else:
            prompt = f"""
Analyse the notice below using ONLY the information provided.
Do not invent dates, deadlines, locations, fees, or requirements.
If a detail is missing, write "Not specified in the notice".

Return these sections:
1. TL;DR — a short plain-language summary
2. Important dates and deadlines
3. Who should pay attention
4. Actions students need to take
5. Missing or unclear information

Notice:
{notice}
"""
            with st.spinner("Reading and summarising the notice..."):
                result = ask_ai(prompt)
            st.markdown("### 🧠 Notice analysis")
            st.markdown(result)

            st.download_button(
                "⬇️ Download summary",
                data=result,
                file_name="campus_notice_summary.txt",
                mime="text/plain"
            )

# ---------- CAMPUS EVENTS ----------
elif page == "📅 Campus Events":
    st.markdown("## 📅 Campus Events")
    st.write("Explore sample events. These are not verified official listings.")

    categories = sorted(set(e["category"] for e in st.session_state.events))
    selected_category = st.selectbox(
        "Filter by category",
        ["All categories"] + categories
    )

    for event in st.session_state.events:
        if (selected_category == "All categories"
                or event["category"] == selected_category):
            with st.container(border=True):
                st.markdown(f"### ✨ {event['name']}")
                st.caption(f"{event['category']}  •  {event['date']}")
                st.write(event["description"])

    st.divider()
    st.markdown("### ➕ Add a demo event")
    with st.form("event_form", clear_on_submit=True):
        event_name = st.text_input("Event name")
        event_category = st.selectbox(
            "Category", ["Technology", "Learning", "Culture", "Sports", "Other"]
        )
        event_date = st.text_input(
            "Date or status", placeholder="e.g. To be announced"
        )
        event_description = st.text_area("Event description")
        submitted_event = st.form_submit_button("Add event")

        if submitted_event:
            if event_name.strip() and event_description.strip():
                st.session_state.events.append({
                    "name": event_name.strip(),
                    "category": event_category,
                    "date": event_date.strip() or "Date not specified",
                    "description": event_description.strip()
                })
                st.success("Demo event added!")
                st.rerun()
            else:
                st.warning("Please enter the event name and description.")

# ---------- LOST AND FOUND ----------
elif page == "🔎 Lost & Found":
    st.markdown("## 🔎 Campus Lost & Found")
    st.write("Report a missing item or something you found.")

    with st.form("lost_found_form", clear_on_submit=True):
        report_type = st.radio(
            "Report type",
            ["Lost item", "Found item"],
            horizontal=True
        )
        item_name = st.text_input(
            "Item name", placeholder="e.g. Black water bottle"
        )
        location = st.text_input(
            "Last seen / found at", placeholder="e.g. Library"
        )
        details = st.text_area(
            "Description", placeholder="Colour, brand, or other useful details"
        )
        contact = st.text_input(
            "Contact information (optional)",
            placeholder="Use only information you are comfortable sharing"
        )
        submitted_report = st.form_submit_button("Submit demo report")

        if submitted_report:
            if item_name.strip() and location.strip() and details.strip():
                st.session_state.reports.insert(0, {
                    "type": report_type,
                    "item": item_name.strip(),
                    "location": location.strip(),
                    "details": details.strip(),
                    "contact": contact.strip(),
                    "time": datetime.now().strftime("%d %b %Y, %I:%M %p")
                })
                st.success("Your report has been added to this demo session.")
                st.rerun()
            else:
                st.warning("Please fill in item name, location, and description.")

    st.divider()
    st.markdown("### 📋 Recent reports")

    if not st.session_state.reports:
        st.info("No reports yet. Add a demo report using the form above.")
    else:
        for report in st.session_state.reports:
            with st.container(border=True):
                st.markdown(f"### {report['type']}: {report['item']}")
                st.caption(
                    f"Location: {report['location']}  •  {report['time']}"
                )
                st.write(report["details"])
                if report["contact"]:
                    st.write(f"Contact: {report['contact']}")

    st.caption(
        "Demo limitation: reports are stored only in this running session. "
        "They are not sent to college staff or saved in a permanent database."
    )

# ---------- CAMPUS FAQs ----------
elif page == "❓ Campus FAQs":
    st.markdown("## ❓ Student Quick Help")

    faqs = {
        "How should I prepare for my first hackathon?":
            "Understand the problem, build a small working prototype, "
            "divide tasks among teammates, test your demo, and practise "
            "a short explanation of the problem and solution.",
        "How can I start learning coding?":
            "Start with Python variables, data types, if/else, loops, "
            "functions, and lists. Practise a little each day and build "
            "small projects as you learn.",
        "How can I make my project presentation better?":
            "Explain the problem first, show your working demo, explain "
            "what makes it useful, mention limitations honestly, and "
            "finish with what you would build next.",
        "What should I include in a project demo?":
            "Include the problem statement, target users, main features, "
            "a live demonstration, the technology used, limitations, "
            "and future improvements.",
        "How do I work well in a team?":
            "Agree on roles, keep tasks small, share progress regularly, "
            "test features together, and make sure everyone understands "
            "the final demo."
    }

    for question, answer in faqs.items():
        with st.expander(question):
            st.write(answer)

st.markdown("---")
st.markdown(
    '<p class="small-muted">CAMPUSBUDDY AI • CYBERPUNK DEMO • '
    'LOCAL MODEL: OLLAMA</p>',
    unsafe_allow_html=True
)
