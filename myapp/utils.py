#from pdf2docx import Converter
import fitz
import tempfile
import io
import os
import base64
from docx import Document

def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    pdf_buffer = pdf_file.read()  

    with fitz.open("pdf", pdf_buffer) as pdf:
        
        num_pages = pdf.page_count

        # I Set the batch size (number of pages to process at once)
        batch_size = 100

        # Iterate through the pages in batches
        for start_page in range(0, num_pages, batch_size):
            end_page = min(start_page + batch_size, num_pages)

            # Extract text from the current batch of pages
            batch_text = ""
            for page_number in range(start_page, end_page):
                page = pdf[page_number]
                batch_text += page.get_text()

            pdf_text += batch_text

    return pdf_text

def convert_pdf_to_docx(pdf_file):

    pdf_text = extract_text_from_pdf(pdf_file)

    doc = Document()

    doc.add_paragraph(pdf_text)

    # Save the DOCX document to a BytesIO buffer
    docx_buffer = io.BytesIO()
    doc.save(docx_buffer)
    docx_buffer.seek(0)

    # Encode the DOCX content in Base64
    docx_content = base64.b64encode(docx_buffer.read()).decode('utf-8')

    return docx_content