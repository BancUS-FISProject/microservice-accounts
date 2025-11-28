from pydantic import BaseModel

class CreateCardRequest(BaseModel):
    name: str

class CreateCardResponse(BaseModel):
    pan: str
    
class DeleteCardRequest(BaseModel):
    pan: str
    
class DeleteCardResponse(BaseModel):
    pan: str