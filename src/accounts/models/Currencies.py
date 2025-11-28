from pydantic import BaseModel

class CurrenciesResponse(BaseModel):
    from_currency: str
    to_currency: str
    original_amount: float
    converted_amount: float