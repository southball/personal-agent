from pydantic import BaseModel
from datetime import datetime

class Patch(BaseModel):
    applied_at: datetime
    patch: str

class Note(BaseModel):
    id: str
    current: dict
    patches: list[Patch]
