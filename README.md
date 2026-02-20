# Paper Knowledge Base (Deepseek + LangChain)

This project builds a local knowledge base over a folder of PDF papers. It uses a local embedding model for retrieval and Deepseek's official API for generation with citations.

## Prerequisites
- Python 3.10 or 3.11
- CUDA GPU recommended (16GB VRAM works well)
- A Deepseek API key

## Quick start
1) Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2) Put your PDFs under `data/papers/`.

3) Set your API key:

```bash
set DEEPSEEK_API_KEY=your_key_here
```

4) Build the vector database:

```bash
python src/ingest.py
```

5) Ask questions:

```bash
python src/query.py "你们课题组近三年主要研究方向是什么？"
```

## Notes
- Metadata is derived from the PDF filename. Recommended format:
  `YYYY-FirstAuthor-ShortTitle.pdf`
- Citations are built from metadata: title, year, and page number.

## Configuration
Edit `configs/settings.yaml` to adjust model names, chunk sizes, and retrieval settings.
