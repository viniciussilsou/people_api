import uvicorn
from fastapi import FastAPI

from connectors.db import create_session
from models import Person, Address
from request_models.person import PersonRequest

app = FastAPI()


@app.get("/persons/{personId}")
async def get_person(personId: int):
    session = create_session()
    query = session.query(Person).filter_by(id=personId)
    person = query.first()
    return person


@app.post("/person")
async def create_person(person: PersonRequest):

    new_address = Address()
    new_address.country = person.address.country

    new_person = Person()
    new_person.name = person.name
    new_person.document_number = person.document_number
    new_person.phone = person.phone
    new_person.address = new_address

    session = create_session()
    session.add(new_person)
    session.commit()

    return new_person


@app.put("/persons/{personId}")
async def update_person(personId: int, person: PersonRequest):
    session = create_session()
    query = session.query(Person).filter_by(id=personId)
    person_to_update = query.first()

    person_to_update.name = person.name
    person_to_update.document_number = person.document_number
    person_to_update.phone = person.phone
    if not person_to_update.address:
        new_address = Address()
        new_address.country = person.address.country
        person_to_update.address = new_address
    else:
        person_to_update.address.country = person.address.country

    session.add(person_to_update)
    session.commit()

    return person_to_update


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
