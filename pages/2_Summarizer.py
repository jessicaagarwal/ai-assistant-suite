import os
import textwrap
import streamlit as st
from utils import get_groq_client
import pdfplumber

# ------------------------------------------------------------------
# Init
# ------------------------------------------------------------------
client = get_groq_client()

st.title("📝 AI Text Summarizer")
st.write("Paste text or upload a file to get a summary. Powered by **LLaMA‑3 (Groq)**.")

# ------------------------------------------------------------------
# Sidebar Settings
# ------------------------------------------------------------------
st.sidebar.header("⚙️ Summary Settings")

length_choice = st.sidebar.radio(
    "Summary Length",
    ["Short", "Medium", "Detailed"],
    index=0,
    help="Controls how much detail appears in the summary."
)

tone_choice = st.sidebar.selectbox(
    "Tone",
    ["Neutral", "Simple", "Professional", "Casual", "Kid-friendly"],
    index=0
)

format_choice = st.sidebar.selectbox(
    "Output Format",
    ["Bullets", "Paragraph", "Bullets + Paragraph", "TL;DR"],
    index=0
)

temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.4)

# ------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------
def build_length_instruction(length: str) -> str:
    if length == "Short":
        return "Give a very short summary in 3 bullet points. Max ~40 words total."
    if length == "Medium":
        return "Give 5 concise bullet points followed by a short paragraph (~100 words)."
    return "Give a detailed summary: key bullet points, a short paragraph (~150 words), and a 1-line takeaway."

def build_tone_instruction(tone: str) -> str:
    mapping = {
        "Neutral": "Use a neutral, informative tone.",
        "Simple": "Use plain language, easy to understand.",
        "Professional": "Use clear, professional language suitable for a report.",
        "Casual": "Use a friendly, conversational tone.",
        "Kid-friendly": "Explain in very simple words, like to a 10-year-old.",
    }
    return mapping.get(tone, "Use a neutral tone.")

def build_format_instruction(fmt: str) -> str:
    mapping = {
        "Bullets": "Output bullet points only.",
        "Paragraph": "Output one short paragraph only.",
        "Bullets + Paragraph": "Start with bullet points, then a short paragraph.",
        "TL;DR": "Output a single TL;DR line.",
    }
    return mapping.get(fmt, "Output bullet points only.")

def truncate_text(txt: str, max_chars: int = 8000) -> str:
    """Prevent overly long payloads. Trim and warn."""
    if len(txt) <= max_chars:
        return txt
    st.warning(f"Input truncated to {max_chars} characters to fit model context.")
    return txt[:max_chars]

# ------------------------------------------------------------------
# Input: Text or File
# ------------------------------------------------------------------
uploaded_file = st.file_uploader("📂 Upload a file (TXT or PDF)", type=["txt", "pdf"])
user_text = ""

if uploaded_file:
    if uploaded_file.type == "text/plain":
        user_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            user_text = "\n".join(pages)

else:
    user_text = st.text_area(
        "Paste text to summarize:",
        height=300,
        placeholder="Paste an article, blog, report, or notes here..."
    )

# ------------------------------------------------------------------
# Summarize Button
# ------------------------------------------------------------------
if st.button("Summarize"):
    clean_text = user_text.strip()
    if not clean_text:
        st.error("Please paste some text or upload a file.")
        st.stop()

    # Build instructions
    length_instr = build_length_instruction(length_choice)
    tone_instr = build_tone_instruction(tone_choice)
    format_instr = build_format_instruction(format_choice)

    # Final prompt
    prompt = textwrap.dedent(f"""
    You are a helpful summarization assistant.
    {length_instr}
    {tone_instr}
    {format_instr}

    Text to summarize:
    {truncate_text(clean_text)}
    """).strip()

    with st.spinner("Summarizing..."):
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            messages=[
                {"role": "system", "content": "You summarize text accurately and follow formatting instructions exactly."},
                {"role": "user", "content": prompt},
            ],
        )
        summary = resp.choices[0].message.content or "[No response]"

    st.subheader("📘 Summary")
    st.markdown(summary)

    # Download button
    st.download_button(
        "⬇️ Download Summary",
        summary,
        file_name="summary.txt",
        mime="text/plain"
    )
