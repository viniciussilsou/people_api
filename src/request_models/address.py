from pydantic import BaseModel

class AddressRequest(BaseModel):
    country: str
