import streamlit as st

from config import model
from backend.utils import extract_pdf_text
from backend.jd_match import match_resume_with_jd


st.title("🎯 ATS Matcher")

# ============================
# Sidebar
# ============================
with st.sidebar:

    st.header("🎯 ATS Matcher")

    st.info(
        """
### How to use

1. Upload your resume (PDF).
2. Upload the job description (PDF or TXT).
3. Click **Compare Resume**.
4. Review the ATS analysis.
"""
    )

st.write(
    "Upload a resume and a job description to receive an AI-powered ATS compatibility analysis."
)

# ============================
# Resume Upload
# ============================

st.header("📄 Resume")

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"],
    key="resume"
)

# ============================
# Job Description Upload
# ============================

st.header("📋 Job Description")

uploaded_jd = st.file_uploader(
    "Upload Job Description",
    type=["pdf", "txt"],
    key="jd"
)

# ============================
# Process Resume
# ============================

if uploaded_resume:

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

        st.error(
            "❌ Unable to process the uploaded resume."
        )

        with st.expander("Technical Details"):
            st.code(str(e))

        st.stop()

    with st.expander("Resume Text"):
        st.text(resume_text)

# ============================
# Process Job Description
# ============================

if uploaded_jd:

    try:

        jd_text = extract_pdf_text(uploaded_jd)

        if not jd_text.strip():
            raise ValueError(
                "No readable text found in the uploaded job description."
            )

    except ValueError as e:

        st.error(f"❌ {e}")
        st.stop()

    except Exception as e:

        st.error(
            "Unable to process the uploaded job description."
        )

        with st.expander("Technical Details"):
            st.code(str(e))

        st.stop()

    with st.expander("Job Description"):
        st.text(jd_text)

# ============================
# Compare Resume
# ============================
if not (uploaded_resume and uploaded_jd):
    st.info(
        "📌 Upload both the resume and the job description to enable comparison."
    )

compare = st.button(
    "🔍 Compare Resume",
    type="primary",
    disabled=not (uploaded_resume and uploaded_jd)
)

if compare:
    with st.spinner(
            "🤖 AI is comparing the resume with the job description..."
    ):

            try:

                comparison = match_resume_with_jd(
                    model,
                    resume_text,
                    jd_text
                )

            except RuntimeError as e:

                st.error(f"❌ {e}")

                with st.expander("Technical Details"):
                    st.code(str(e.__cause__))

                st.stop()

            st.success("✅ ATS analysis completed successfully!")

            st.metric(
            "🎯 ATS Match Score",
            f"{comparison['match_score']}%"
            )

            st.progress(comparison["match_score"] / 100)

            with st.container(border=True):

                st.subheader("📝 Reasoning")
                st.write(comparison["reasoning"])

                st.subheader("✅ Matching Skills")

                if comparison["matching_skills"]:
                    for skill in comparison["matching_skills"]:
                        st.write(f"• {skill}")
                else:
                    st.write("No matching skills identified.")

                st.subheader("❌ Missing Skills")

                if comparison["missing_skills"]:
                    for skill in comparison["missing_skills"]:
                        st.write(f"• {skill}")
                else:
                    st.write("No major missing skills identified.")

                st.subheader("💪 Strengths")

                if comparison["strengths"]:
                    for strength in comparison["strengths"]:
                        st.write(f"• {strength}")
                else:
                    st.write("No strengths identified.")

                st.subheader("⚠️ Weaknesses")

                if comparison["weaknesses"]:
                    for weakness in comparison["weaknesses"]:
                        st.write(f"• {weakness}")
                else:
                    st.write("No weaknesses identified.")

                st.subheader("📈 Suggestions")

                if comparison["suggestions"]:
                    for suggestion in comparison["suggestions"]:
                        st.write(f"• {suggestion}")
                else:
                    st.write("No suggestions available.")

                st.subheader("🎯 Recommendation")
                st.info(comparison["recommendation"])

                st.divider()

