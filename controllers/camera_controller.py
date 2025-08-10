# Iosif Vieru
# 9 Aug. 2025

from fastapi import (
    APIRouter, HTTPException, Request
)

from persistance.schemas import CameraDataSchema
from services.camera_service import (
    insert_camera, get_data_from_all_cameras, get_camera_data_by_id
)

MAX_LENGTH = 64
OBJECTID_LENGTH = 24
router = APIRouter()

def generate_hateoas_links(request: Request, resource_id: str):
    links = {
        "self": {
            "href": str(request.url_for("get_camera_information", id=resource_id)),
            "method": "GET"
        },
        "parent": {
            "href": str(request.url_for("get_all_camera_data")),
            "method": "GET"
        },
        "update": {
            "href": str(request.url_for("get_camera_information", id=resource_id)),
            "method": "PUT"
        },
        "delete": {
            "href": str(request.url_for("get_camera_information", id=resource_id)),
            "method": "DELETE"
        }
    }

    return links

@router.get('/api/cameras')
async def get_all_camera_data(
    request: Request,
    city: str | None = None,
    road: str | None = None
    ):

    params = {}

    if city != None:
        params["city"] = city

    if road != None:
        params["road"] = road

    result = get_data_from_all_cameras(params)

    if result is None:
        raise HTTPException(status_code=503, detail="Failed to get the data.")

    if not result:
        raise HTTPException(status_code=404, detail="No camera data found.")

    # adding HATEOAS link for every element
    for r in result:
        r["_links"] = generate_hateoas_links(request, r["_id"])

    return {
        "cameras": result,
        "_links": "HATEOAS COMING SOON."
    }

@router.get('/api/cameras/{id}')
async def get_camera_information(
    request: Request, 
    id: str
    ):
    
    if(len(id) != OBJECTID_LENGTH):
        raise HTTPException(status_code=422, detail="ID must be a 24-character hex string.")
    
    response = get_camera_data_by_id(id)

    if response is None:
        raise HTTPException(status_code=503, detail="Failed to get the data.")

    if not response:
        raise HTTPException(status_code=404, detail="No camera found with this id.")

    links = generate_hateoas_links(request, id)

    return {
        "camera": dict(response),
        "_links": links
    }

@router.post('/api/cameras')
async def insert_new_camera(request: Request, data: CameraDataSchema):
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

    # inserting the data to persistance
    result = insert_camera(data)
    if result is None:
        raise HTTPException(status_code=503, detail=f"Failed to insert data.")

    links = generate_hateoas_links(request, result["_id"])

    return {
        "camera": result,
        "_links": links
    }