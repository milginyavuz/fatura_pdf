# PDF Invoice Splitter with OCR

This project is a Python automation script that splits multi-page PDF files containing multiple invoices into separate PDF files based on detected invoice numbers.

It uses OCR and text pattern matching to automatically identify and extract each individual invoice.

## Features
- Splits multi-page PDF files into single-page documents  
- Converts PDF pages to images for OCR processing  
- Extracts invoice numbers using Tesseract OCR  
- Detects invoice numbers using regular expressions  
- Saves each invoice as a separate PDF file named by invoice number  

## Technologies
- Python  
- PyPDF2  
- pdf2image  
- Tesseract OCR (pytesseract)  
- Regular Expressions (regex)  

## Usage
1. Place the input PDF file in the project directory  
2. Run the script:
   ```bash
   python pdf_fatura_ayir.py
