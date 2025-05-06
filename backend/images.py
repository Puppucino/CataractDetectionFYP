from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Header
from jose import jwt, JWTError
from database import SessionLocal
from models import Image, User
import os
import shutil
import subprocess
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as image_module
import numpy as np

router = APIRouter()
JWT_SECRET = os.getenv("JWT_SECRET")
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load models once at startup
LENET_MODEL_PATH = os.getenv("LENET_MODEL_PATH")
MOBILENET_MODEL_PATH = os.getenv("MOBILENET_MODEL_PATH")
lenet5_model = load_model(LENET_MODEL_PATH)
mobilenetv2_model = load_model(MOBILENET_MODEL_PATH)

async def get_db():
    async with SessionLocal() as db:
        yield db

async def get_current_user(authorization: str = Header(...), db=Depends(get_db)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid user")
        return user
    except (JWTError, IndexError):
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/upload")
async def upload_image(image: UploadFile = File(...), user=Depends(get_current_user), db=Depends(get_db)):
    save_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    # In-memory inference
    # Preprocess for LeNet5 (128x128, grayscale)
    img_lenet = image_module.load_img(save_path, target_size=(128, 128), color_mode='grayscale')
    x_lenet = image_module.img_to_array(img_lenet)
    x_lenet = np.expand_dims(x_lenet, axis=0)
    x_lenet = x_lenet / 255.0
    # Preprocess for MobileNetV2 (128x128, RGB)
    img_mobilenet = image_module.load_img(save_path, target_size=(128, 128), color_mode='rgb')
    x_mobilenet = image_module.img_to_array(img_mobilenet)
    x_mobilenet = np.expand_dims(x_mobilenet, axis=0)
    x_mobilenet = x_mobilenet / 255.0
    # Predict probabilities
    p1 = lenet5_model.predict(x_lenet, verbose=0)[0][0]
    p2 = mobilenetv2_model.predict(x_mobilenet, verbose=0)[0][0]
    p_ensemble = (p1 + p2) / 2
    # Ensemble result
    threshold = 0.5
    prediction = f"Cataract (confidence: {p_ensemble:.2f})" if p_ensemble >= threshold else f"Healthy (confidence: {p_ensemble:.2f})"
    img = Image(user_id=user.id, filename=image.filename, prediction=prediction)
    db.add(img)
    await db.commit()
    return {"prediction": prediction, "imageUrl": f"/uploads/{image.filename}"}

@router.get("/history")
async def get_history(user=Depends(get_current_user), db=Depends(get_db)):
    result = await db.execute(select(Image).where(Image.user_id == user.id).order_by(Image.created_at.desc()))
    images = result.scalars().all()
    return [{
        "filename": img.filename,
        "prediction": img.prediction,
        "created_at": img.created_at.isoformat() if img.created_at else None
    } for img in images] 