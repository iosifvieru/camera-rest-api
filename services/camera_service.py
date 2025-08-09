# Iosif Vieru
# 9 Aug. 2025

from persistance.schemas import CameraDataSchema
from persistance.database import get_database

db = get_database('camera_data')
collection = db.get_collection('cameras')

def insert_camera(data: CameraDataSchema):
    data_as_dict = data.model_dump()

    query_result = collection.insert_one(dict(data_as_dict))

    result = {
        "_id": str(query_result.inserted_id)
    } | data_as_dict

    return result