# Iosif Vieru
# 9 Aug. 2025

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import camera_controller

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://unde-sunt-camere.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""]
)

app.include_router(camera_controller.router)
