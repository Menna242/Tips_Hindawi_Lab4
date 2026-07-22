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
<img width="1835" height="897" alt="image" src="https://github.com/user-attachments/assets/fa2e9301-4dd1-441a-94f0-7874d5211833" />
<img width="1746" height="890" alt="image" src="https://github.com/user-attachments/assets/86060694-7e86-49e5-a0c4-c174d66c7605" />
<img width="1800" height="857" alt="image" src="https://github.com/user-attachments/assets/6928ea26-e0b1-4241-a56d-46d1681caf50" />


