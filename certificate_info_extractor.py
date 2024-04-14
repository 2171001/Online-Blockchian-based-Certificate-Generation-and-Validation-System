import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    
    Args:
    - pdf_path (str): Path to the PDF file.
    
    Returns:
    - str: Extracted text from the PDF.
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        num_pages = reader.numPages
        for page_num in range(num_pages):
            page = reader.getPage(page_num)
            text += page.extractText()
    return text

def extract_certificate_info(text):
    """
    Extract necessary information from the certificate text.
    
    Args:
    - text (str): Text extracted from the PDF certificate.
    
    Returns:
    - str: Formatted information extracted from the certificate.
    """
    print("Extracting certificate information...")
    print("Certificate text:")
    print(text)
    
    certificate_info = {}
    
    # Example: Extracting certificate holder name
    holder_name_match = re.search(r"certifies that\s+([^\n]+)\s+has", text, re.IGNORECASE)
    print("Holder name match:", holder_name_match)
    if holder_name_match:
        certificate_info["Holder Name"] = holder_name_match.group(1).strip()
    else:
        certificate_info["Holder Name"] = "Holder name not found."
    
    # Example: Extracting issue date
    issue_date_match = re.search(r"(Issue Date:|CERTIFICATION DATE:|DIRECTOR OF [^\n]+)\s*([a-zA-Z]+ \d{1,2}, \d{4})", text, re.IGNORECASE)
    print("Issue date match:", issue_date_match)
    if issue_date_match:
        certificate_info["Issue Date"] = issue_date_match.group(2)
    else:
        certificate_info["Issue Date"] = "Issue date not found."
    
    # Format the extracted information
    formatted_info = f"Holder Name: {certificate_info['Holder Name']}\n"
    formatted_info += f"Issue Date: {certificate_info['Issue Date']}\n"
    
    return formatted_info

# Prompt user for PDF path
pdf_path = input("Enter the full path of the PDF certificate file: ")

# Extract text from the PDF
certificate_text = extract_text_from_pdf(pdf_path)

# Extract certificate information
certificate_info = extract_certificate_info(certificate_text)

# Print extracted certificate information
print("Extracted Certificate Information:")
print(certificate_info)
