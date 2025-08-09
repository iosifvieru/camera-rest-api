# Iosif Vieru
# 9 Aug. 2025

from fastapi import FastAPI
from controllers import camera_controller
from contextlib import asynccontextmanager

app = FastAPI()

app.include_router(camera_controller.router)

@app.get('/')
def hello_world():
    return {
        "message": "Hello world!"
    }
