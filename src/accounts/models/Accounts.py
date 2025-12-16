from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional, List

from .Cards import CardInfo


class AccountBase(BaseModel):
    name: str
    iban: str
    cards: List[CardInfo] = Field(default_factory=list)
    creation_date: datetime = Field(default_factory=datetime.now)
    email: str
    subscription: str
    subscription_end_date: datetime = Field(default_factory=datetime.now)
    balance: float = 0
    isBlocked: bool = False

class AccountCreate(BaseModel):
    name: str
    email: str
    subscription: str

class AccountUpdateBalance(BaseModel):
    balance: float

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    subscription: Optional[str] = None
    
class AccountView(BaseModel):
    name: str
    iban: str
    cards: List[CardInfo]
    creation_date: datetime
    email: str
    subscription: str
    balance: float
    isBlocked: bool
    
class AccountListResponse(BaseModel):
    items: List[AccountView] = Field(..., description="La lista de cuentas de la página solicitada")
    total: int = Field(..., description="El número total de cuentas que existen en la base de datos (sin paginar)")
    page: int = Field(..., description="El número de página actual")
    size: int = Field(..., description="El número de elementos por página (limit)")
