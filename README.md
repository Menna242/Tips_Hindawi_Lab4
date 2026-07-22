# 📄 Resume Information Extractor

A Streamlit web app that extracts structured information (name, email, education, skills, and experience) from PDF resumes using a locally-hosted LLM (Mistral-Nemo-Instruct) served from Kaggle via an ngrok tunnel.

## 🧠 How It Works

This project runs in two parts:

1. **Kaggle (Backend / Model Server)**
   Loads the `Mistral-Nemo-Instruct-2407` model on a free Kaggle GPU, wraps it in a FastAPI `/generate` endpoint, and exposes it to the internet using an ngrok tunnel.

2. **Local Machine (Frontend / Client)**
   A Streamlit app that:
   - Accepts a PDF resume upload
   - Extracts the raw text using `PyPDFLoader`
   - Builds a structured prompt using LangChain's `PromptTemplate` and `StructuredOutputParser`
   - Sends the prompt to the Kaggle-hosted model through the ngrok URL
   - Parses the model's JSON response into structured fields
   - Displays the result and allows downloading it as a `.json` file

```
┌─────────────────────┐         ┌──────────────────────┐
│   Kaggle Notebook     │         │   Local Machine        │
│                        │         │                        │
│  • Mistral-Nemo model  │◄────────│  • Streamlit UI        │
│  • FastAPI server      │  ngrok  │  • PDF reading         │
│  • ngrok tunnel        │  tunnel │  • Prompt building     │
│                        │         │  • JSON parsing        │
└─────────────────────┘         └──────────────────────┘
```
