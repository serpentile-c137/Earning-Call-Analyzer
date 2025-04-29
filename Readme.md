# Earning-Call-Analyzer

1. Developed an AI-Powered Earnings Call Summarization Tool
Engineered a Python-based application that utilizes Google’s GenAI API to generate concise summaries of earnings call transcripts, enhancing the efficiency of financial analysis.

2. Integrated Streamlit for User-Friendly Interface
Implemented a Streamlit front-end, enabling users to upload transcript files and receive real-time, AI-generated summaries through an intuitive web interface.

3. Managed Secure API Key Handling with dotenv
Employed the python-dotenv package to securely manage API keys, ensuring best practices in handling sensitive information within the development environment.

4. Utilized Temporary File Handling for Efficient Processing
Leveraged Python’s tempfile module to handle user-uploaded files efficiently, facilitating seamless integration with the AI summarization pipeline.


## Installation

1. Clone this repository to your local machine using:
```bash
git clone https://github.com/serpentile-c137/Earning-Call-Analyzer.git
cd Earning Call Analyzer
```

2. Install libraries
```bash
pip install -r requirements
```

3. Set up your Gemini API key by creating a .env file in the project root and adding your API
```bash
GOOGLE_API_KEY=your_api_key
```

4. Run the Streamlit app
```bash
streamlit run main.py
```

#### Project Url : https://earning-call-analyzer.streamlit.app/
