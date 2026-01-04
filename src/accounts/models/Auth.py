from pydantic import BaseModel


class CreaterAuthUser(BaseModel):
    #iban: str  todo esto hay que ponerlo, auth NO PUEDE CREAR EL IBAN
    email: str
    name: str
    password: str
    phoneNumber: str
