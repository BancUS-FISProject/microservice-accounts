from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EmptyDelete200(BaseModel):
    """
    OK
    """
    pass

class EmptyPatch204(BaseModel):
    """
    No content
    """
    pass

class EmptyDelete204(BaseModel):
    """
    No content
    """
    pass


class EmptyGet400(BaseModel):
    """
    Bad Request
    """
    pass

class EmptyPatch400(BaseModel):
    """
    Bad Request
    """
    pass

class EmptyPost400(BaseModel):
    """
    Bad Request
    """
    pass

class EmptyDelete400(BaseModel):
    """
    Bad Request
    """
    pass

class EmptyPatch403(BaseModel):
    """
    Forbidden Operation - Not sufficient funds
    """
    pass

class EmptyGet404(BaseModel):
    """
    Account not found
    """
    pass

class EmptyPatch404(BaseModel):
    """
    Account not found
    """
    pass

class EmptyPost404(BaseModel):
    """
    Account not found
    """
    pass

class EmptyDelete404(BaseModel):
    """
    Account not found
    """
    pass

class EmptyError503(BaseModel):
    """
    Service Unavailable
    """
    pass