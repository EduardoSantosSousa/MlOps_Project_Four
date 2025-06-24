import io
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import torch
from torchvision import models, transforms
from PIL import Image, ImageDraw
from src.model_architecture import FasterRCNNModel
from config.paths_config import MODEL_PATH
from contextlib import asynccontextmanager

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    print("🔄 Carregando modelo...")
    loaded_model = FasterRCNNModel(num_classes=2, device=device).model
    loaded_model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    loaded_model.to(device)
    loaded_model.eval()
    model = loaded_model
    print("✅ Modelo carregado com sucesso!")
    yield  # aqui começa o app
    print("🛑 Finalizando aplicação")


app = FastAPI(lifespan=lifespan)

#app = FastAPI()

#model_path = MODEL_PATH
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#model = FasterRCNNModel(num_classes=2, device=device).model
#model.load_state_dict(torch.load(model_path, map_location=device))

#model.to(device)
#model.eval()

transforms = transforms.Compose([
    transforms.ToTensor(),  

])


def predict_and_draw(image: Image.Image):
    
    img_tensor = transforms(image).unsqueeze(0).to(device)

    with torch.no_grad():
        predictions = model(img_tensor)

    prediction = predictions[0]
    boxes = prediction['boxes'].cpu().numpy()
    labels = prediction['labels'].cpu().numpy()
    scores = prediction['scores'].cpu().numpy()

    img_rgb = image.convert("RGB")

    draw = ImageDraw.Draw(img_rgb)

    for box, score in zip(boxes,scores):
        if score > 0.7:
            x_min, y_min, x_max, y_max = box
            draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=2)

    return img_rgb


@app.get("/")
def read_root():
    return{"message": "Welcome to the Guns Object Detection API"}



@app.post("/predict/")
async def predict(file:UploadFile=File(...)):

    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))

    output_image = predict_and_draw(image)

    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")





