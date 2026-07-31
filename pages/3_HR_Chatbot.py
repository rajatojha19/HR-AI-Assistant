import streamlit as st

from config import model
from backend.chatbot import hr_chat


st.title("💬 HR Chatbot")

# ============================
# Sidebar
# ============================

with st.sidebar:

    st.header("💬 HR Chatbot")

    st.info(
        """
### How to use

Ask questions about:

- HR Interviews
- Technical Interviews
- Resume Tips
- Career Guidance
- Communication Skills

Example Questions:

• Tell me about yourself.
• What are your strengths?
• Explain OOP.
• Difference between JOIN and UNION.
• What is normalization?
"""
    )

# ============================
# Welcome Message
# ============================

st.info(
    "👋 Welcome! I'm your AI HR Interview Assistant. Ask me anything related to interviews, resumes, career guidance, or technical interview preparation."
)

# ============================
# User Input
# ============================

question = st.text_area(
    "Ask an HR or interview-related question",
    height=120,
    placeholder="Example: Tell me about yourself."
)

ask = st.button(
    "💬 Ask HR Assistant",
    type="primary",
)

# ============================
# Generate Response
# ============================

if ask:

    if not question.strip():
        st.warning("⚠ Please enter a question.")
        st.stop()

    with st.spinner("🤖 HR Assistant is thinking..."):

        try:

            answer = hr_chat(
                model,
                question
            )

        except RuntimeError as e:

            st.error(f"❌ {e}")

            with st.expander("Technical Details"):
                st.code(str(e.__cause__))

            st.stop()

    st.success("✅ Response generated successfully!")

    with st.container(border=True):

        st.subheader("🙋 Your Question")
        st.write(question)

        st.divider()

        st.subheader("🤖 HR Assistant")
        st.write(answer)

        st.divider()

