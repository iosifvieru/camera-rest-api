# Iosif Vieru
# 9 Aug. 2025
from pydantic import BaseModel
from typing import Optional

class CameraDataSchema(BaseModel):
    city: str
    road: str
    location: str
    longitude: float
    latitude: float
    description: Optional[str] = None