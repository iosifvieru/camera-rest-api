# Iosif Vieru
# 9 Aug. 2025

from fastapi import (
    APIRouter, HTTPException
)

from persistance.schemas import CameraDataSchema
from services.camera_service import (
    insert_camera
)

MAX_LENGTH = 64
router = APIRouter()

@router.get('/api/cameras')
def get_all_camera_data():
    return "OK"

@router.post('/api/cameras')
def insert_new_camera(data: CameraDataSchema):
    if len(data.city) == 0:
        raise HTTPException(status_code=422, detail="City length cannot be zero!")

    if len(data.city) > MAX_LENGTH:
        raise HTTPException(status_code=422, detail=f"City length cannot be longer than {MAX_LENGTH}!")

    if len(data.road) == 0:
        raise HTTPException(status_code=422, detail="Road length cannot be zero!")
    
    if len(data.road) > MAX_LENGTH:
        raise HTTPException(status_code=422, detail=f"Road length cannot be greater than {MAX_LENGTH}!")

    if len(data.location) == 0:
        raise HTTPException(status_code=422, detail="Location length cannot be zero!")
    
    if len(data.location) > MAX_LENGTH:
        raise HTTPException(status_code=422, detail=f"Location length cannot be greater than {MAX_LENGTH}!")

    result = insert_camera(data)

    return {
        "camera": result,
        "_links": "HATEOAS INCOMING."
    }