import os
import fitz  # PyMuPDF
import requests
import streamlit as st
import tempfile
import arxiv

# ====== CONFIG ======
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD2wwJeg6vIQUTH1TTqUrtQ*****")
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# ====== PDF PARSER ======
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

# ====== GEMINI LLM CALL ======
def query_gemini(context, user_query):
    prompt = f"""You are a research assistant. Use the following content to answer the user question.

Content:
\"\"\"
{context}
\"\"\"

Question: {user_query}
Answer:"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(GEMINI_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"

# ====== ARXIV API ======
def search_arxiv(query):
    results = arxiv.Search(query=query, max_results=3)
    return "\n\n".join([f"🔹 {r.title}\n{r.entry_id}" for r in results.results()])

# ====== STREAMLIT UI ======
st.set_page_config(page_title="Document Q&A AI Agent", layout="wide")
st.title("📄 Document Q&A AI Agent ")

uploaded_files = st.file_uploader("Upload PDF Documents", type=["pdf"], accept_multiple_files=True)
documents = {}

if uploaded_files:
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        text = extract_text_from_pdf(tmp_path)
        documents[file.name] = text
    st.success(f"{len(uploaded_files)} document(s) uploaded and parsed.")

query = st.text_input("Enter your question (e.g., 'Summarize Paper A', 'Find papers on quantum transformers')")

if st.button("Get Answer") and query:
    if "find papers" in query.lower():
        arxiv_results = search_arxiv(query)
        st.markdown("### 🔎 Arxiv Results")
        st.text(arxiv_results)
    elif documents:
        combined_context = "\n\n".join(documents.values())
        answer = query_gemini(combined_context, query)
        st.markdown("### 💡 Answer")
        st.write(answer)
    else:
        st.warning("Please upload PDF documents first.")
