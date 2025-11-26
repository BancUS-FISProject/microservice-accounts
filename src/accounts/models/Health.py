from datetime import datetime
from pydantic import BaseModel, Field

class Healthy(BaseModel):
    status: str = "UP"
    service: str = "Accounts"
    
class Starting(BaseModel):
    status: str = "STARTING"
    service: str = "Accounts"
    detail: str = "Connecting to resources..."