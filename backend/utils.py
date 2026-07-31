from PyPDF2 import PdfReader

def extract_pdf_text(pdf_file):
    """
    Extract all readable text from a PDF file.

    Args:
        pdf_file: Uploaded PDF file.

    Returns:
        A string containing the extracted text.
    """

    reader = PdfReader(pdf_file)

    pages = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            pages.append(page_text)

    return "\n\n".join(pages)