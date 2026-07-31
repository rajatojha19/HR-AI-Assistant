import streamlit as st

st.set_page_config(
    page_title="HR AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ============================
# Header
# ============================

st.title("🤖 HR AI Assistant")

st.subheader("Your Intelligent HR & Career Assistant")

st.write(
    "Empower job seekers and recruiters with AI-driven tools for "
    "resume analysis, ATS matching, HR interview preparation, and "
    "company policy assistance—all in one intelligent platform."
)

st.divider()

# ============================
# Features
# ============================

st.subheader("🚀 Features")

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):
        st.markdown("### 📄 Resume Analyzer")
        st.write(
            "Analyze resumes using Gemini AI and receive detailed feedback, strengths, weaknesses, and improvement suggestions."
        )

    with st.container(border=True):
        st.markdown("### 💬 HR Chatbot")
        st.write(
            "Ask HR interview, technical interview, resume, and career-related questions with AI-powered responses."
        )

with col2:

    with st.container(border=True):
        st.markdown("### 🎯 ATS Matcher")
        st.write(
            "Compare resumes with job descriptions and receive an ATS compatibility score with personalized recommendations."
        )

    with st.container(border=True):
        st.markdown("### 📚 HR Policy Q&A")
        st.write(
            "Upload company policy documents and ask questions using Retrieval-Augmented Generation (RAG)."
        )

st.divider()

# ============================
# Technologies
# ============================

st.subheader("🛠 Technologies Used")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.success("🤖 Google Gemini AI")
    st.success("🧠 LangChain")
    st.success("🔍 FAISS")

with tech2:
    st.success("📄 PyPDF2")
    st.success("📊 Sentence Transformers")
    st.success("⚡ Streamlit")

with tech3:
    st.success("🐍 Python")
    st.success("🧮 NumPy")
    st.success("💻 VS Code")

st.divider()

# ============================
# How to Use
# ============================

st.subheader("📖 How to Use")

st.info(
    """
1. Select a module from the **sidebar**.
2. Upload the required document (if applicable).
3. Click the action button.
4. Review the AI-generated results.
"""
)

# ============================
# Footer
# ============================

st.divider()

st.caption("Developed by Rajat Ojha | Powered by Google Gemini AI • Streamlit • LangChain • FAISS")
