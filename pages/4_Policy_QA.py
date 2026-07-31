import streamlit as st
import hashlib

from backend.rag import (
    load_policy,
    create_index,
    answer_question
)

st.set_page_config(
    page_title="HR Policy Q&A",
    page_icon="📚"
)

st.title("📚 HR Policy Q&A")

# ============================
# Sidebar
# ============================
with st.sidebar:

    st.header("📚 HR Policy Assistant")

    st.info(
        """
### How to use

1. Upload a company policy PDF.
2. Wait for the document to be processed.
3. Ask questions related to the policy.
4. Receive AI-powered answers.
"""
    )

# ============================
# Session State
# ============================
if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "embeddings" not in st.session_state:
    st.session_state.embeddings = None

if "index" not in st.session_state:
    st.session_state.index = None

if "uploaded_file_hash" not in st.session_state:
    st.session_state.uploaded_file_hash = None

# ============================
# File Upload
# ============================
uploaded_policy = st.file_uploader(
    "Upload Company Policy",
    type=["pdf"]
)

if uploaded_policy:

    # Create hash of uploaded PDF
    file_bytes = uploaded_policy.getvalue()
    current_hash = hashlib.sha256(file_bytes).hexdigest()

    # Process only if the uploaded file is different
    if st.session_state.uploaded_file_hash != current_hash:

        progress = st.progress(0)
        status = st.empty()

        status.info("📄 Reading PDF...")
        progress.progress(25)

        try:

            chunks, embeddings = load_policy(uploaded_policy)

            status.info("📚 Building FAISS Index...")
            progress.progress(75)

            index = create_index(embeddings)

        except ValueError as e:

            st.error(f"❌ {e}")

            progress.empty()
            status.empty()

            st.stop()

        except Exception as e:

            st.error(
                "❌ Unable to process the uploaded PDF. "
                "Please upload a valid text-based PDF."
            )

            with st.expander("Technical Details"):
                st.code(str(e))

            progress.empty()
            status.empty()

            st.stop()

        progress.progress(100)
        status.success("✅ Policy processed successfully!")

        # Save into session state
        st.session_state.chunks = chunks
        st.session_state.embeddings = embeddings
        st.session_state.index = index
        st.session_state.uploaded_file_hash = current_hash

        # Remove progress widgets
        progress.empty()
        status.empty()

    else:
        st.success("⚡ Using cached document.")

    # Retrieve cached objects
    chunks = st.session_state.chunks
    embeddings = st.session_state.embeddings
    index = st.session_state.index

    # ============================
    # Document Information
    # ============================
    
    with st.expander("📄 Document Information"):

        st.write("**Document Name:**", uploaded_policy.name)
        st.write("**Chunks Created:**", len(chunks))

    st.divider()

    # ============================
    # Question Input
    # ============================
    # ============================
# Question Input
# ============================

question = st.text_input(
    "Ask a question about the policy",
    placeholder="Example: What is the internship duration?"
)

ask = st.button(
    "🔍 Ask Policy Assistant",
    type="primary",
)

if ask:

    if uploaded_policy is None:
        st.warning("⚠ Please upload a company policy PDF first.")
        st.stop()

    if not question.strip():
        st.warning("⚠ Please enter a question.")
        st.stop()

    with st.status(
        "Processing your question...",
        expanded=True
    ) as status:

        status.write("🔎 Searching relevant policy sections...")

        try:

            answer, sources = answer_question(
                question,
                index,
                chunks
            )

        except RuntimeError as e:

            st.error(f"❌ {e}")

            with st.expander("Technical Details"):
                st.code(str(e.__cause__))

            st.stop()

        status.update(
            label="✅ Answer generated successfully!",
            state="complete",
            expanded=False
        )

    st.subheader("🤖 Answer")

    with st.container(border=True):
        st.write(answer)

    st.subheader("📄 Relevant Policy Sections")

    for i, source in enumerate(sources, start=1):

        with st.expander(
            f"📄 Source {i}",
            expanded=(i == 1)
        ):
            st.write(source)

    st.divider()

    st.caption(
        "🤖 HR AI Assistant | Powered by Google Gemini, FAISS & Streamlit"
    )