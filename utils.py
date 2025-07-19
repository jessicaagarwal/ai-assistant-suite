import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load .env only once
load_dotenv()

@st.cache_resource(show_spinner=False)
def get_groq_client() -> Groq:
    """Return a cached Groq client using key from secrets or env."""
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ GROQ_API_KEY missing. Add to .env or Streamlit Secrets.")
        st.stop()
    return Groq(api_key=api_key)
