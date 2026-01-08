import os
import sys
import pytesseract
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image
import tempfile
import re

# tesseract'ı portable dizinden çalıştır
tesseract_path = os.path.join(os.path.dirname(sys.executable), "tesseract", "Tesseract-OCR", "tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract_text_from_pdf_page(image: Image.Image) -> str:
    return pytesseract.image_to_string(image, lang="tur+eng")

def extract_invoice_number(text: str) -> str:
    patterns = [
        r"Fatura ID[:\s]*([A-Z0-9\-]+)",
        r"E-?Fatura No[:\s]*([A-Z0-9\-]+)",
        r"Fatura No[:\s]*([A-Z0-9\-]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def split_pdf_by_invoice_id(pdf_path: str, output_dir: str):
    reader = PdfReader(pdf_path)
    temp_dir = tempfile.mkdtemp()

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(output_dir, base_name)
    os.makedirs(output_folder, exist_ok=True)

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        temp_pdf_path = os.path.join(temp_dir, f"temp_page.pdf")

        with open(temp_pdf_path, "wb") as temp_pdf:
            writer.write(temp_pdf)

        images = convert_from_path(temp_pdf_path)
        if images:
            text = extract_text_from_pdf_page(images[0])
            invoice_number = extract_invoice_number(text)

            if invoice_number:
                filename = f"{invoice_number}.pdf"
                final_path = os.path.join(output_folder, filename)
                with open(final_path, "wb") as out_pdf:
                    writer.write(out_pdf)

def main():
    if len(sys.argv) < 2:
        print("PDF dosya yolu belirtilmedi.")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print("PDF dosyası bulunamadı.")
        sys.exit(1)

    output_dir = os.path.dirname(pdf_path)
    split_pdf_by_invoice_id(pdf_path, output_dir)
    print("Fatura sayfaları başarıyla ayrıldı.")

if __name__ == "__main__":
    main()
