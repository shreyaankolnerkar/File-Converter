import os
import tempfile

from pdf2docx import Converter


def pdf_to_docx(pdf_bytes: bytes) -> bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_tmp:
        pdf_tmp.write(pdf_bytes)
        pdf_path = pdf_tmp.name

    docx_path = pdf_path.replace(".pdf", ".docx")

    cv = Converter(pdf_path)
    cv.convert(docx_path)
    cv.close()

    with open(docx_path, "rb") as f:
        docx_bytes = f.read()

    os.remove(pdf_path)
    os.remove(docx_path)

    return docx_bytes
