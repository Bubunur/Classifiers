import io
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError
from transformers import pipeline

BASE_DIR = Path(__file__).parent
models = {}
NEWS_LABELS = {0: "Business", 1: "Sports", 2: "Sci/Tech"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    models["image"] = pipeline("image-classification", model="Bubunur/animals-classifier")
    models["text"] = pipeline("text-classification", model="Bubunur/ag-news-classifier")
    yield
    models.clear()


app = FastAPI(title="Classifiers", lifespan=lifespan)


@app.post("/api/classify/text")
def classify_text(text: str = Form(...)):
    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Текст не должен быть пустым")
    results = models["text"](text, top_k=None)
    for r in results:
        idx = int(str(r["label"]).rsplit("_", 1)[-1])
        r["label"] = NEWS_LABELS.get(idx, r["label"])
    return results


@app.post("/api/classify/image")
async def classify_image(file: UploadFile = File(...)):
    data = await file.read()
    try:
        image = Image.open(io.BytesIO(data)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Файл не является изображением")
    return models["image"](image, top_k=5)

app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static")
