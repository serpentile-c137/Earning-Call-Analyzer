import streamlit as st
import tempfile
import os
from typing import List
from google import genai
from dotenv import load_dotenv
import os
from collections import defaultdict

load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY', 'your-key-if-not-using-env')
client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

# --- Define the core functions ---
def summarize_earnings_call_stream(file_path: str, prompt: str = None) -> str:
    if prompt is None:
        prompt = '''
You are a professional financial analyst.
Given the following earnings call transcript, please perform the following tasks:

Summarize the key financial highlights, including revenue, earnings per share (EPS), guidance, and any notable changes or trends.

Identify major themes and strategic initiatives discussed by the management.

Note any significant commentary from the Q&A session, especially from analysts.

Provide an Executive Summary that captures the overall sentiment of the call (positive, neutral, negative), key takeaways for investors, and any potential risks or opportunities mentioned.

Make the short descriptive summary concise, professional, and suitable for a report to senior executives or investors.
        '''
        prompt = "You are a financial analyst. Please summarize and provide an executive summary of the earnings call transcript."

    uploaded_file = client.files.upload(file=file_path)
    response = client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=[uploaded_file, prompt]
    )
    for chunk in response:
        yield chunk.text

def extract_financial_numbers_stream(file_path: str) -> str:
    prompt = '''
You are a financial analyst.
Given the following earnings call transcript, please extract all key financial numbers and metrics mentioned in the document.

Instructions:

Focus only on data provided within the transcript. Do not refer to or incorporate any external sources.

Include figures such as revenue, earnings per share (EPS), net income, gross margin, operating margin, guidance (current and forward-looking), capital expenditures, free cash flow, and any other relevant financial metrics.

Organize the extracted data in a clear, structured format (e.g., bullet points or a table) for easy reference.

Compare the figures of companies within the same industry or sector, if applicable.

Make sure the output is accurate and includes units (e.g., millions, billions, percentages) where applicable.
'''
    uploaded_file = client.files.upload(file=file_path)
    response = client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=[uploaded_file, prompt]
    )
    for chunk in response:
        yield chunk.text

def analyze_qna_sentiment_stream(file_path: str) -> str:
    prompt = '''
You are a financial analyst with expertise in sentiment analysis.
Given the Q&A section of the following earnings call transcript, perform a sentiment analysis focused specifically on management's responses.

Instructions:

Analyze the tone, language, and content of management’s replies during the Q&A.

Determine whether the overall management sentiment is positive, negative, or neutral.

Support your assessment with specific examples or quotes that illustrate the sentiment.

Highlight any changes in tone based on the type of questions (e.g., around guidance, costs, growth, or competitive landscape).

Provide a concise, professional summary suitable for inclusion in an investor briefing
'''
    uploaded_file = client.files.upload(file=file_path)
    response = client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=[uploaded_file, prompt]
    )
    for chunk in response:
        yield chunk.text


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
                        result = summarize_earnings_call_stream(tmp_path)
                        st.subheader(f"📄 Summary: {uploaded_file.name}")
                        st.write(result)
                    elif financial_btn:
                        result = extract_financial_numbers_stream(tmp_path)
                        st.subheader(f"💰 Financial Numbers: {uploaded_file.name}")
                        st.write(result)
                    elif sentiment_btn:
                        result = analyze_qna_sentiment_stream(tmp_path)
                        st.subheader(f"🧠 Sentiment Analysis: {uploaded_file.name}")
                        st.write(result)
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")
                finally:
                    os.remove(tmp_path)
