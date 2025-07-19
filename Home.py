import streamlit as st

st.set_page_config(
    page_title="AI Multi-Tool Platform",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 AI Multi-Tool Platform")
st.write(
    """
    Welcome! This platform bundles **three AI apps** powered by **Groq LLaMA‑3**:

    - **🤖 Chatbot** – Conversational assistant with personalization.
    - **📝 Summarizer** – Condense long text or PDFs with tone & length control.
    - **🔍 JSON Extractor** – Pull structured data (Name, Email, Phone, etc.) from messy text.

    Use the cards below or the **Pages sidebar** to open a tool.
    """
)

st.divider()

# Try to detect if Streamlit supports programmatic page switching
HAS_SWITCH = hasattr(st, "switch_page")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Chat", value="🤖")
    if HAS_SWITCH:
        if st.button("Open Chatbot"):
            st.switch_page("pages/1_Chatbot.py")
    else:
        st.caption("Use sidebar → Chatbot.")

with col2:
    st.metric(label="Summarize", value="📝")
    if HAS_SWITCH:
        if st.button("Open Summarizer"):
            st.switch_page("pages/2_Summarizer.py")
    else:
        st.caption("Use sidebar → Summarizer.")

with col3:
    st.metric(label="Extract", value="🔍")
    if HAS_SWITCH:
        if st.button("Open JSON Extractor"):
            st.switch_page("pages/3_JSON_Extractor.py")
    else:
        st.caption("Use sidebar → JSON Extractor.")

st.divider()

st.info("Don’t see buttons? Use the **Pages** section in the left sidebar to navigate between tools.")

st.markdown(
    """
    ---
    **Built with ❤️ by Jessica Agarwal.** 
    """
)
