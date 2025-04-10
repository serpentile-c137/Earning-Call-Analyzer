import streamlit as st
import tempfile
import os
from typing import List
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY', 'your-key-if-not-using-env')
client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

# --- Define the core functions ---
def summarize_earnings_call(file_path: str, prompt: str = None) -> str:
    if prompt is None:
        prompt = "You are a financial analyst. Please summarize and provide an executive summary of the earnings call transcript."
    
    # client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])
    uploaded_file = client.files.upload(file=file_path)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[uploaded_file, prompt]
    )
    return response.text

def extract_financial_numbers(file_path: str) -> str:
    prompt = "Extract all key financial numbers and metrics from this earnings call transcript. Do not refer to any other sources."
    # client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])
    uploaded_file = client.files.upload(file=file_path)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[uploaded_file, prompt]
    )
    return response.text

def analyze_qna_sentiment(file_path: str) -> str:
    prompt = "Analyze the sentiment of the Q&A section of this earnings call transcript. Highlight if management sentiment is positive, negative, or neutral."
    client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])
    uploaded_file = client.files.upload(file=file_path)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[uploaded_file, prompt]
    )
    return response.text

# --- Streamlit UI ---
st.set_page_config(page_title="Earnings Call Analysis", layout="wide")
st.title("📊 Earnings Call PDF Analyzer")

uploaded_files = st.file_uploader("Upload earnings call PDF(s)", type=["pdf"], accept_multiple_files=True)

col1, col2, col3 = st.columns(3)

with col1:
    summarize_btn = st.button("📄 Summarize Earnings Call")
with col2:
    financial_btn = st.button("💰 Extract Financial Numbers")
with col3:
    sentiment_btn = st.button("🧠 Q&A Sentiment Analysis")

if not uploaded_files:
    st.warning("Please upload at least one PDF file.")
else:
    if summarize_btn or financial_btn or sentiment_btn:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                # Save to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                try:
                    if summarize_btn:
                        result = summarize_earnings_call(tmp_path)
                        st.subheader(f"📄 Summary: {uploaded_file.name}")
                        st.write(result)
                    elif financial_btn:
                        result = extract_financial_numbers(tmp_path)
                        st.subheader(f"💰 Financial Numbers: {uploaded_file.name}")
                        st.write(result)
                    elif sentiment_btn:
                        result = analyze_qna_sentiment(tmp_path)
                        st.subheader(f"🧠 Sentiment Analysis: {uploaded_file.name}")
                        st.write(result)
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")
                finally:
                    os.remove(tmp_path)
