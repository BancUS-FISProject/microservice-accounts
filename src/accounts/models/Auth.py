from pydantic import BaseModel


class CreaterAuthUser(BaseModel):
    iban: str
    email: str
    name: str
    password: str
    phoneNumber: str
