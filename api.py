from fastapi import FastAPI, UploadFile, File
from pdf2image import convert_from_bytes
from paddleocr import PaddleOCR
import tempfile

app = FastAPI()
ocr_engine = PaddleOCR(use_angle_cls=True, lang='pt', use_space_char=True, show_log=False, structure_version='PP-Structure', layout=True)

@app.get("/")
def health():
    return {"status": "API running", "info": "Use POST /ocr-table to process PDF"}

@app.post("/ocr-table")
async def ocr_table(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "O arquivo deve ser um PDF"}

    pdf_bytes = await file.read()

    with tempfile.TemporaryDirectory() as tmpdir:
        images = convert_from_bytes(pdf_bytes, fmt='png', output_folder=tmpdir)
        results = []

        for idx, img in enumerate(images):
            result = ocr_engine.ocr(img, cls=True, det=True, rec=True, structure=True)
            text = [item[1][0] for block in result if isinstance(block, list) for item in block if len(item) > 1]
            results.append({
                "page": idx + 1,
                "text": "\n".join(text),
                "structure": result
            })

    return {"pages": results}
