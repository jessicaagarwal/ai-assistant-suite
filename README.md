# 🤖 AI Multi-Tool Platform (Chatbot + Summarizer + JSON Extractor)

A **AI platform** powered by **Groq API (LLaMA-3)**.  
This platform combines three powerful tools in a single interface:

1. **AI Chatbot** – Chat like ChatGPT with mood personalization.  
2. **AI Text Summarizer** – Summarize long texts with custom tone & length.  
3. **AI JSON Extractor** – Extract structured data (e.g., Name, Email, Phone) as JSON.

---

## 🚀 Live Demo
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-assistant-suite.streamlit.app/)

---

## ✨ Features  
✅ **Multi-Tool Platform** – Chatbot, Summarizer, and JSON Extractor in one app.  
✅ **Personalized Chatbot** – Add your name, mood, and few-shot examples.  
✅ **Smart Text Summarizer** – Custom summary length, tone, and format.  
✅ **Dynamic JSON Extractor** – Select custom fields, file upload, and download JSON.  
✅ **File Upload Support** – TXT and PDF input support.  
✅ **Dark UI with Emojis** – Friendly and interactive interface.  
✅ **Secure API Management** – Using `.env` or Streamlit Secrets.  

---

## 🛠 Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **LLM Provider:** Groq API (LLaMA-3 models)
- **Extras:** pdfplumber, python-dotenv

---

## 📂 Project Structure
```
├── Home.py                  # Main entry (Dashboard)
├── utils.py                 # Utility functions
├── pages/
│   ├── 1_Chatbot.py        # AI Chatbot Tool
│   ├── 2_Summarizer.py     # AI Text Summarizer
│   ├── 3_JSON_Extractor.py # AI JSON Extractor
├── README.md
├── requirements.txt
├── .gitignore
└── .env.example
```

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/jessicaagarwal/ai-assistant-suite.git
cd ai-assistant-suite
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate    # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 API Setup

### 1. Get Groq API Key
- Visit [Groq Console](https://console.groq.com/keys)
- Copy your API key

### 2. Local Development
Create `.env` file in project root:
```
GROQ_API_KEY=your_api_key_here
```

### 3. Streamlit Cloud Deployment
- Add your key in **Streamlit Secrets**:
```
GROQ_API_KEY="your_api_key_here"
```

---

## ✅ requirements.txt
```
streamlit
python-dotenv
groq
pdfplumber
PyPDF2
python-docx
httpx==0.27.0
```

---

## ▶️ Run the App
```bash
streamlit run app.py
```
App will run at:
```
http://localhost:8501
```

---

## 📚 Resources
- [Groq API Docs](https://console.groq.com/docs)
- [Streamlit Docs](https://docs.streamlit.io)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

---

## 🔥 Future Enhancements
- Export **chat history & summaries**.
- Add **speech-to-text & text-to-speech**.
- Multi-LLM Support (Gemini, Claude, OpenAI).
- Add **Analytics Dashboard**.

---

### ⭐ If you like this project, give it a star on GitHub!
