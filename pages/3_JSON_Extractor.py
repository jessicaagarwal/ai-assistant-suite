import os
import json
import streamlit as st
from utils import get_groq_client
import pdfplumber

# -------------------------------------------------------------
# Init
# -------------------------------------------------------------
client = get_groq_client()

st.title("🔍 AI JSON Extractor")
st.write("Paste unstructured text or upload a file, then choose the fields to extract.")

# -------------------------------------------------------------
# Sidebar Fields
# -------------------------------------------------------------
st.sidebar.header("⚙️ JSON Fields")
default_fields = ["Name", "Email", "Phone"]
fields_input = st.sidebar.text_area(
    "Enter fields (comma-separated):",
    value=", ".join(default_fields),
    help="Example: Name, Email, Phone, Address, Company"
)

selected_fields = [f.strip() for f in fields_input.split(",") if f.strip()]

# -------------------------------------------------------------
# Input: File or Text
# -------------------------------------------------------------
uploaded_file = st.file_uploader("📂 Upload a file (TXT or PDF)", type=["txt", "pdf"])

if uploaded_file:
    if uploaded_file.type == "text/plain":
        user_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            user_text = "\n".join(pages)
else:
    user_text = st.text_area(
        "Paste your text here:",
        height=250,
        placeholder="Paste an email, resume, or paragraph..."
    )

# -------------------------------------------------------------
# Extract JSON
# -------------------------------------------------------------
if st.button("Extract JSON"):
    if not user_text.strip():
        st.error("Please provide text for extraction.")
        st.stop()

    json_schema = "{\n" + ",\n".join([f'    "{f.lower()}": "..."' for f in selected_fields]) + "\n}"

    prompt = f"""
    Extract the following details from the text:
    {", ".join(selected_fields)}

    Return ONLY valid JSON in this format:
    {json_schema}

    Text:
    {user_text}
    """

    with st.spinner("Extracting JSON..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0,
                messages=[
                    {"role": "system", "content": "You extract structured data and output ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content.strip()

            def extract_json(text: str) -> dict:
                text = text.strip().replace("```json", "").replace("```", "")
                return json.loads(text)

            try:
                parsed_json = extract_json(result)
                st.subheader("✅ Extracted JSON")
                st.json(parsed_json)

                st.download_button(
                    label="⬇️ Download JSON",
                    data=json.dumps(parsed_json, indent=4),
                    file_name="extracted_data.json",
                    mime="application/json"
                )

            except json.JSONDecodeError:
                st.error("⚠️ The model returned invalid JSON after cleaning. Raw output below:")
                st.code(result, language="json")

        except Exception as e:
            st.error(f"Error: {e}")
