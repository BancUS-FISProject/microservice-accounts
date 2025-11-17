from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List

# Base account data
class AccountBase(BaseModel):
    name: str
    iban: str
    cards: List[str]
    creation_date: datetime
    email: str
    subscription: str
    funds: int
    isBlocked: bool

# Account update data needed
class AccountCreate(BaseModel):
    name: str
    email: str
    subscription: Optional[str] = None

# Account update funds data needed
class AccountUpdateFunds(BaseModel):
    iban: str
    funds: int

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    subscription: Optional[str] = None
    
class AccountView(BaseModel):
    name: str
    iban: str
    cards: List[str]
    creation_date: datetime
    email: str
    subscription: str
    funds: int
    isBlocked: bool
    pass