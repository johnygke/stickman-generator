# Stickman Origami Generator with GPT-Image-1 and GCS

This Streamlit app lets you:
- Upload prompts via CSV
- Enhance prompts using GPT-4o
- Generate pastel stickman images with GPT-Image-1 or CE.SDK
- Upload the final images to Google Cloud Storage

## Setup
1. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

Make sure to set your environment variables in `.env` or Streamlit Cloud secrets.