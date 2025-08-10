# Iosif Vieru
# 9 Aug. 2025

from persistance.schemas import CameraDataSchema
from persistance.database import get_database
from bson.objectid import ObjectId
from bson.son import SON

db = get_database('camera_data')
collection = db.get_collection('cameras')

def insert_camera(data: CameraDataSchema):
    data_as_dict = data.model_dump()
    
    if collection is None:
        return None

    query_result = collection.insert_one(dict(data_as_dict))

    result = {
        "_id": str(query_result.inserted_id)
    } | data_as_dict

    return result

def get_data_from_all_cameras(params: dict):
    response = []

    if collection is None:
        return None

    cursor = None

    if params is None:
        cursor = collection.find({})
    else:
        cursor = collection.find(SON(params))

    if cursor is None:
        return None

    for item in cursor:
        camera_data = {
            "_id": str(item["_id"]),
        } | dict(CameraDataSchema(**item))

        response.append(camera_data)

    return response

def get_camera_data_by_id(id: str):
    if collection is None:
        return None

    result = collection.find_one({"_id": ObjectId(id)})
    result["_id"] = str(result["_id"])

    return result