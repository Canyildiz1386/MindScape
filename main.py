import pytesseract

# If tesseract is not in your PATH, specify the full path to the executable
pytesseract.pytesseract.tesseract_cmd = '/opt/local/bin/tesseract'

from PIL import Image

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        gray_image = image.convert('L')
        extracted_text = pytesseract.image_to_string(gray_image)
        return extracted_text
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
image_path = "image.png"
extracted_text = extract_text_from_image(image_path)
print("Extracted Text:", extracted_text)
