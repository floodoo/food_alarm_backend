from fastapi import FastAPI, UploadFile
from datetime import datetime
from ocr import OCR
import fasttext

app = FastAPI()
PRETRAINED_MODEL_PATH = "../fast_text/lid.176.bin"
model = fasttext.load_model(PRETRAINED_MODEL_PATH)


@app.get("/food-alarm/get-expiry-date")
async def get_expiry_date(file: UploadFile):
    try:
        ocr_text = OCR(file.file).get_ocr_text_pytessearct()

        possible_dates = []
        date = None

        language_result = model.predict(text=ocr_text)
        print(language_result)

        for word in ocr_text.split():
            if len(word) > 8:
                continue

            if language_result[0][0] == "__label__de":
                try:
                    date = datetime.strptime(word, "%d.%M.%y").strftime("%d.%M.%Y")

                except ValueError:
                    pass

                try:
                    date = datetime.strptime(word, "%d.%M.%Y").strftime("%d.%M.%Y")

                except ValueError:
                    pass

            try:
                date = datetime.strptime(word, "%d/%M/%y").strftime("%d/%M/%Y")

            except ValueError:
                pass

            try:
                date = datetime.strptime(word, "%d/%M/%Y").strftime("%d/%M/%Y")

            except ValueError:
                pass

            if date is not None:
                possible_dates.append(date)

        possible_dates.sort()

        return {"possible_expiry_date": possible_dates[0]}

    except Exception as e:
        print(e)
        return {"error": e}
