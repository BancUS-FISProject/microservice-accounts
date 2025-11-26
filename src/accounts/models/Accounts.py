from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional, List

# Base account data
class AccountBase(BaseModel):
    name: str
    iban: str
    cards: List[str] = Field(default_factory=list)
    creation_date: datetime = Field(default_factory=datetime.now)
    email: str
    subscription: str
    balance: float = 0
    isBlocked: bool = False
    # todo add subscription end date instead of field subscription
    # tier1subscriptionend
    # tier2subscriptionend

# Account update data needed
class AccountCreate(BaseModel):
    name: str
    email: str
    subscription: str

# Account update balance data needed
class AccountUpdatebalance(BaseModel):
    balance: float

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
    balance: float
    isBlocked: bool
    pass