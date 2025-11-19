from datetime import datetime

from pydantic import BaseModel, Field

class CreateCardRequest(BaseModel):
    name: str

class CreateCardResponse(BaseModel):
    pan: str
    
class DeleteCardRequest(BaseModel):
    pan: str
    
class DeleteCardResponse(BaseModel):
    pan: str