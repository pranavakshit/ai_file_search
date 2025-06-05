import os
import docx
from PyPDF2 import PdfReader

def extract_text_from_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    return [
        {"file": os.path.basename(path), "position": f"Line {i+1}", "text": line.strip()}
        for i, line in enumerate(lines) if line.strip()
    ]

def extract_text_from_pdf(path):
    reader = PdfReader(path)
    results = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        for line in text.splitlines():
            if line.strip():
                results.append({
                    "file": os.path.basename(path),
                    "position": f"Page {i+1}",
                    "text": line.strip()
                })
    return results

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return [
        {"file": os.path.basename(path), "position": f"Paragraph {i+1}", "text": para.text.strip()}
        for i, para in enumerate(doc.paragraphs) if para.text.strip()
    ]

def scan_files_and_extract_text(folder_path):
    all_data = []
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        if filename.lower().endswith(".txt"):
            all_data.extend(extract_text_from_txt(path))
        elif filename.lower().endswith(".pdf"):
            all_data.extend(extract_text_from_pdf(path))
        elif filename.lower().endswith(".docx"):
            all_data.extend(extract_text_from_docx(path))
    return all_data
