import streamlit as st

# Set page config
st.set_page_config(
    page_title="AI Multi-Tool Platform",
    page_icon="🚀",
    layout="centered"
)

# Landing Page Content
st.title("🚀 AI Multi-Tool Platform")
st.write(
    """
    Welcome to the **AI Multi-Tool Platform** – a one-stop solution with multiple AI-powered utilities:
    
    - **🤖 Chatbot** – Talk with LLaMA-3
    - **📝 Summarizer** – Summarize any text or article
    - **🔍 JSON Extractor** – Extract structured JSON data

    Use the sidebar or the navigation menu to switch between tools.
    """
)

st.info("Select a tool from the **Pages** section on the left sidebar to get started.")
