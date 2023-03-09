from PIL import Image
from pytesseract import pytesseract
from google.cloud import vision


class OCR:
    def __init__(self, image):
        self.image = image

    def get_ocr_text_pytessearct(self):
        image = Image.open(self.image)
        ocr_text = pytesseract.image_to_string(image)

        return ocr_text

    def get_ocr_text_google_vision(self):
        client = vision.ImageAnnotatorClient()
        binary_file = self.image.read()
        vision_image = vision.Image(content=binary_file)
        vision_response = client.text_detection(image=vision_image)
        response_text_annotations = vision_response.text_annotations

        ocr_text = [text.description for text in response_text_annotations]

        ocr_text = ocr_text[0]
        ocr_text = ocr_text.replace("'", "")
        ocr_text = ocr_text.replace(",", "")

        return ocr_text
