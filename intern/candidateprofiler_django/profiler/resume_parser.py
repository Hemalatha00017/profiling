import re
from pdfminer.high_level import extract_text

def extract_resume_data(file):
    text = extract_text(file)
    return {
        "full_name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
    }

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group() if match else ""

def extract_phone(text):
    match = re.search(r'\+?\d[\d -]{8,12}\d', text)
    return match.group() if match else ""

def extract_linkedin(text):
    match = re.search(r'linkedin\.com/in/[A-Za-z0-9_-]+', text)
    return f"https://{match.group()}" if match else ""

def extract_github(text):
    match = re.search(r'github\.com/[A-Za-z0-9_-]+', text)
    return f"https://{match.group()}" if match else ""

def extract_name(text):
    lines = text.strip().split("\n")
    return lines[0].strip() if lines else ""
