FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    libgl1 \
    git && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    paddleocr \
    paddlepaddle \
    fastapi \
    uvicorn \
    pdf2image \
    python-multipart \
    opencv-python \
    shapely \
    numpy \
    scikit-image \
    PyMuPDF

WORKDIR /app

COPY api.py .

EXPOSE 5000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]
