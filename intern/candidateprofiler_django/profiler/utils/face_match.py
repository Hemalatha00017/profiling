# File: profiler/utils/face_match.py

# File: profiler/utils/face_match.py

from deepface import DeepFace
import os
import tempfile
import requests
from PIL import Image
from io import BytesIO
import pytesseract

def compare_faces(img1_file, img2_file):
    """
    Compare two face images and return similarity score (0–100).

    Parameters:
    - img1_file: InMemoryUploadedFile (from Django form upload or file stream)
    - img2_file: Can also be an InMemoryUploadedFile or bytes object

    Returns:
    - similarity: float score (0 to 100)
    """
    try:
        # Save both images to temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp1, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp2:

            # Write contents to the temporary files
            temp1.write(img1_file.read())
            temp2.write(img2_file.read())
            temp1.flush()
            temp2.flush()

            # Run DeepFace verification
            result = DeepFace.verify(
                img1_path=temp1.name,
                img2_path=temp2.name,
                model_name="VGG-Face",
                enforce_detection=False,
                detector_backend="opencv"
            )

            distance = result.get("distance", 1.0)
            similarity = max(0, 100 - distance * 100)

        os.unlink(temp1.name)
        os.unlink(temp2.name)

        return round(similarity, 2)

    except Exception as e:
        print(f"[Face Match Error] {e}")
        return 0.0

def compare_with_url(uploaded_image, image_url):
    """
    Download image from URL and compare it with uploaded_image.
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_from_url = BytesIO(response.content)
        return compare_faces(uploaded_image, image_from_url)
    except Exception as e:
        print(f"[Image URL Fetch Error] {e}")
        return 0.0

def extract_text_from_image(image_file):
    """
    Extract text from image using OCR (Tesseract).
    """
    try:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"[OCR Error] {e}")
        return ""

# Sample usage for OCR + comparison:
def match_image_and_extract_text(user_image, profile_image_url):
    similarity = compare_with_url(user_image, profile_image_url)
    extracted_text = extract_text_from_image(user_image)
    return {
        "similarity_score": similarity,
        "ocr_text": extracted_text
    }
