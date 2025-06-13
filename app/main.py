from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select, create_engine

from .models import Record, SQLModel


app = FastAPI()
engine = create_engine("sqlite:///database.db", echo=False)

SQLModel.metadata.create_all(engine)


@app.post("/records/", response_model=Record)
def create_record(record: Record):
    with Session(engine) as session:
        session.add(record)
        session.commit()
        session.refresh(record)
        return record


@app.get("/records/", response_model=list[Record])
def read_records():
    with Session(engine) as session:
        return session.exec(select(Record)).all()


@app.get("/records/{record_id}", response_model=Record)
def read_record(record_id: int):
    with Session(engine) as session:
        record = session.get(Record, record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        return record


@app.put("/records/{record_id}", response_model=Record)
def update_record(record_id: int, item: Record):
    with Session(engine) as session:
        db_item = session.get(Record, record_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Record not found")
        db_item.name = item.name
        db_item.description = item.description
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item


@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    with Session(engine) as session:
        item = session.get(Record, record_id)
        if not item:
            raise HTTPException(status_code=404, detail="Record not found")
        session.delete(item)
        session.commit()
        return {"ok": True}
