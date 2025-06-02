# Document Q&A AI Agent

An enterprise-ready Document Question & Answer AI Agent built using Google Gemini API and Arxiv API.  
This app allows users to upload multiple PDF research papers, extract and query their content using a Large Language Model (LLM), and search for relevant papers on Arxiv.

---

## Features

- Multi-PDF ingestion: Upload multiple PDFs and extract full text with PyMuPDF.
- Contextual Q&A: Ask detailed questions about uploaded documents using Gemini LLM API.
- Summarization & Extraction:Summarize key insights and extract evaluation metrics from papers.
- Arxiv integration: Search and retrieve relevant research papers based on natural language queries.
- Streamlit UI: Interactive and user-friendly web interface.

---


## Setup Instructions

### Prerequisites

- Python 3.8+
- Google Gemini API key (set as `GEMINI_API_KEY` environment variable)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/saitej13sai/Document-Q-A-AI-Agent.git
   cd Document-Q-A-AI-Agent
