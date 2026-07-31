import streamlit as st

from config import model
from backend.resume import analyze_resume
from backend.utils import extract_pdf_text

st.title("📄 Resume Analyzer")

with st.sidebar:

    st.header("📄 Resume Analyzer")

    st.info(
        """
### How to use

1. Upload your resume (PDF).
2. Click **Analyze Resume**.
3. Review the AI analysis.
4. Improve your resume using the suggestions.
"""
    )
st.write(
    "Upload your resume to receive an AI-powered evaluation, strengths, improvement suggestions, and interview recommendations."
)

st.divider()

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"],
    key="resume_analyzer"
)

analyze = st.button(
    "🤖 Analyze Resume",
    type="primary",
)

if analyze:

    if uploaded_resume is None:
        st.warning("⚠ Please upload a PDF resume first.")
        st.stop()

    st.success("✅ Resume uploaded successfully!")

    st.write("**Filename:**", uploaded_resume.name)
    st.write("**File Size:**", f"{uploaded_resume.size / 1024:.2f} KB")

    try:

        resume_text = extract_pdf_text(uploaded_resume)

        if not resume_text.strip():
            raise ValueError(
                "No readable text found in the uploaded resume."
            )

    except ValueError as e:

        st.error(f"❌ {e}")
        st.stop()

    except Exception as e:

        st.error("❌ Unable to process the uploaded resume.")

        with st.expander("Technical Details"):
            st.code(str(e))

        st.stop()

    with st.expander("📄 View Extracted Resume Text"):
        st.text(resume_text)

    with st.spinner("🤖 AI is analyzing your resume..."):

        try:

            analysis = analyze_resume(
                model,
                resume_text
            )

        except Exception as e:

            st.error("❌ Unable to analyze the uploaded resume.")

            with st.expander("Technical Details"):
                st.code(str(e))

            st.stop()

    st.success("✅ Resume analyzed successfully!")

    st.markdown("## 🤖 Resume Analysis")

    with st.container(border=True):
        st.write(analysis)

    st.divider()

