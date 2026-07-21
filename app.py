import streamlit as st
import requests
import tempfile
import re
import json

from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader


# ----------------------------
# API Configuration
# ----------------------------
URL = "https://shrapnel-tastiness-washbasin.ngrok-free.dev/generate"
HEADERS = {"Authorization": "Bearer Menna123"}

# ----------------------------
# Response Schema
# ----------------------------
FullName_schema = ResponseSchema(
    name="full_name",
    description="The full name of the user."
)

email_schema = ResponseSchema(
    name="email",
    description="The email of the user."
)

education_schema = ResponseSchema(
    name="education",
    description="A list of education entries with {degree, institution, year}."
)

skills_schema = ResponseSchema(
    name="skills",
    description="A list of strings."
)

experience_schema = ResponseSchema(
    name="experience",
    description="A list of experiences with {role, company, years}."
)

response_schemas = [
    FullName_schema,
    email_schema,
    education_schema,
    skills_schema,
    experience_schema,
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

# ----------------------------
# Prompt Template
# ----------------------------
User_Information_template = """
You are a smart assistant that extracts user information from a user's description.

Extract:
- Full Name
- Email
- Education
- Skills
- Experience

Respond ONLY in JSON.

{format_instructions}

User Input:
{user_input}
"""


def extract_json_block(text):
    pattern = r"```json\s*(.*?)\s*```"
    matches = re.findall(pattern, text, re.DOTALL)

    if matches:
        return matches[-1]

    return text


# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(
    page_title="Resume Information Extractor",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Resume Information Extractor")

st.write(
    "Upload a PDF resume and extract structured information using your LLM API."
)

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    st.success("PDF uploaded successfully!")

    if st.button("Extract Information"):

        with st.spinner("Reading PDF..."):

            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                pdf_path = tmp.name

            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

            user_input = "\n".join(doc.page_content for doc in documents)

        prompt = PromptTemplate(
            template=User_Information_template,
            input_variables=["user_input", "format_instructions"],
        ).format(
            user_input=user_input,
            format_instructions=format_instructions,
        )

        payload = {
            "prompt": prompt,
            "max_length": 3000,
        }

        with st.spinner("Calling LLM..."):

            try:
                response = requests.post(
                    URL,
                    headers=HEADERS,
                    json=payload,
                )

                response.raise_for_status()

                llm_response = response.json()["response"]

                json_text = extract_json_block(llm_response)

                data = json.loads(json_text)

                st.success("Extraction Complete!")

                st.subheader("Extracted Information")

                st.json(data)

                st.download_button(
                    "Download JSON",
                    json.dumps(data, indent=4),
                    file_name="resume_information.json",
                    mime="application/json",
                )

            except Exception as e:
                st.error(f"Error: {e}")