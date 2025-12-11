from pydantic import BaseModel

class CreateCardRequest(BaseModel):
    cardholderName: str

class CreateCardResponse(BaseModel):
    PAN: str
    
class DeleteCardRequest(BaseModel):
    pan: str
    
class DeleteCardResponse(BaseModel):
    PAN: str
    
class CardInfo(BaseModel):
    pan: str