from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EmptyPatch202(BaseModel):
    """
    No content
    """
    pass

class EmptyDelete204(BaseModel):
    """
    No content
    """
    pass
    
class EmptyGet404(BaseModel):
    """
    Account not found
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

class EmptyPatch403(BaseModel):
    """
    Forbidden Operation - Not sufficient funds
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

class EmptyError503(BaseModel):
    """
    Service Unavailable
    """
    pass