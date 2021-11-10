from pydantic import BaseModel
from request_models.address import AddressRequest


class PersonRequest(BaseModel):
    document_number: int
    name: str
    phone: str
    address: AddressRequest
