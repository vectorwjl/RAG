import os
import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

import fitz
import yaml
from langchain.schema import Document


@dataclass
class Settings:
    data_dir: str
    chroma_dir: str
    collection_name: str
    embedding_model: str
    embedding_device: str
    chunk_size: int
    chunk_overlap: int
    deepseek_base_url: str
    deepseek_model: str
    temperature: float
    top_k: int
    score_threshold: float


def load_settings(path: str) -> Settings:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Settings(**data)


def get_pdf_paths(data_dir: str) -> List[str]:
    if not os.path.isdir(data_dir):
        return []
    return [
        os.path.join(data_dir, name)
        for name in os.listdir(data_dir)
        if name.lower().endswith(".pdf")
    ]


def parse_filename_metadata(filename: str) -> Dict[str, str]:
    base = os.path.splitext(os.path.basename(filename))[0]
    year_match = re.match(r"^(19\d{2}|20\d{2})", base)
    year = year_match.group(1) if year_match else "unknown"
    title = base
    if year_match:
        title = base[len(year_match.group(1)):].lstrip("-_ ")
    return {
        "paper_title": title or base,
        "year": year,
        "source_path": filename,
    }


def _collect_repeated_lines(pages_lines: List[List[str]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for lines in pages_lines:
        uniq = set(line.strip() for line in lines if line.strip())
        for line in uniq:
            counts[line] = counts.get(line, 0) + 1
    return counts


def _clean_page_lines(lines: List[str], repeated: Dict[str, int], page_count: int) -> List[str]:
    cleaned: List[str] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if repeated.get(line, 0) >= max(2, int(page_count * 0.4)):
            continue
        cleaned.append(line)
    return cleaned


def extract_documents_from_pdf(pdf_path: str) -> List[Document]:
    meta = parse_filename_metadata(pdf_path)
    doc = fitz.open(pdf_path)
    pages_lines: List[List[str]] = []
    for page in doc:
        text = page.get_text("text")
        lines = text.splitlines()
        pages_lines.append(lines)

    repeated = _collect_repeated_lines(pages_lines)
    documents: List[Document] = []
    stop_at_references = False

    for idx, lines in enumerate(pages_lines):
        if stop_at_references:
            break
        cleaned = _clean_page_lines(lines, repeated, len(pages_lines))
        page_text = "\n".join(cleaned).strip()
        if not page_text:
            continue

        if re.search(r"\bReferences\b|参考文献", page_text, flags=re.IGNORECASE):
            parts = re.split(r"\bReferences\b|参考文献", page_text, flags=re.IGNORECASE)
            page_text = parts[0].strip()
            stop_at_references = True
            if not page_text:
                continue

        page_meta = dict(meta)
        page_meta["page"] = str(idx + 1)
        documents.append(Document(page_content=page_text, metadata=page_meta))

    return documents


def format_citation(meta: Dict[str, str]) -> str:
    title = meta.get("paper_title", "unknown")
    year = meta.get("year", "unknown")
    page = meta.get("page", "?")
    return f"{title} ({year}) p.{page}"
