import os
os.environ["USE_TF"] = "0"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from images import router as images_router
from deepseek import router as deepseek_router
from medical_qa import router as medical_qa_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cataractdetect-ee566.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth")
app.include_router(images_router, prefix="/api/images")
app.include_router(deepseek_router, prefix="/api/deepseek")
app.include_router(medical_qa_router, prefix="/api/medical")

# Serve uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") 