from datetime import datetime

from pydantic import BaseModel, Field

class CreateCardRequest(BaseModel):
    name: str

class CreateCardResponse(BaseModel):
    pan: str