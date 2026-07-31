import os

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load local .env (for local development)
load_dotenv()

# Try Streamlit Secrets first, then fall back to .env
api_key = st.secrets.get(
    "GEMINI_API_KEY",
    os.getenv("GEMINI_API_KEY")
)

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Please configure Streamlit Secrets or your .env file."
    )

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)