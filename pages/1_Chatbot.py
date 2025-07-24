import json
import streamlit as st
from utils import get_groq_client

# ------------------------------------------------------------------
# Init
# ------------------------------------------------------------------
client = get_groq_client()

st.title("🤖 AI Chatbot")
st.write("Chat with an LLaMA‑3 model via Groq. Personalize tone, mood, and more.")

# ------------------------------------------------------------------
# Sidebar controls
# ------------------------------------------------------------------
st.sidebar.header("⚙️ Chatbot Settings")

user_name = st.sidebar.text_input("👤 Your Name", "")
mood = st.sidebar.selectbox("😊 How are you feeling?", ["Neutral", "Happy", "Sad", "Stressed"])

system_role_input = st.sidebar.text_area("System Role:", "You are a helpful assistant.")
temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.7)
few_shot = st.sidebar.checkbox("Enable Few-Shot Examples")

# Clear chat
with st.sidebar.expander("🧰 Chat Tools", expanded=True):
    if st.button("🗑 Clear Chat"):
        st.session_state.chatbot_messages = []
        st.rerun()

    if st.session_state.get("chatbot_messages"):
        chat_txt = "\n".join([f"{m['role'].title()}: {m['content']}" for m in st.session_state.chatbot_messages])
        chat_json = json.dumps(st.session_state.chatbot_messages, indent=2, ensure_ascii=False)

        st.download_button("⬇ Chat (.txt)", chat_txt, "chat_history.txt", "text/plain")
        st.download_button("⬇ Chat (.json)", chat_json, "chat_history.json", "application/json")

# ------------------------------------------------------------------
# Few-shot examples
# ------------------------------------------------------------------
few_shot_examples = [
    {"role": "user", "content": "What is AI?"},
    {"role": "assistant", "content": "AI stands for Artificial Intelligence. It lets computers perform tasks that seem smart—like answering questions or recognizing images."},
    {"role": "user", "content": "Explain LLM in simple words."},
    {"role": "assistant", "content": "An LLM is a Large Language Model that reads tons of text and learns to respond like a human."},
]

# ------------------------------------------------------------------
# Personalized system role (rebuilt fresh each rerun)
# ------------------------------------------------------------------
system_role = system_role_input.strip()
if user_name:
    system_role += f" Always call the user '{user_name}'."
if mood != "Neutral":
    system_role += f" The user feels {mood}. Respond in an empathetic, encouraging way."

# ------------------------------------------------------------------
# Session state init
# ------------------------------------------------------------------
if "chatbot_messages" not in st.session_state:
    st.session_state.chatbot_messages = []  # only user/assistant turns

# ------------------------------------------------------------------
# Render existing history
# ------------------------------------------------------------------
for msg in st.session_state.chatbot_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------------------------------------------------------
# Chat input
# ------------------------------------------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user turn
    st.session_state.chatbot_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build context
    context = [{"role": "system", "content": system_role}]
    if few_shot:
        context += few_shot_examples
    context += st.session_state.chatbot_messages  # includes latest user

    # LLM call
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=temperature,
                messages=context,
            )
            answer = resp.choices[0].message.content or ""

            # Friendly emoji (dedupe)
            if not answer.startswith("✨"):
                answer = "✨ " + answer

            st.markdown(answer)

    # Save assistant turn
    st.session_state.chatbot_messages.append({"role": "assistant", "content": answer})
