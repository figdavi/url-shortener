from typing import Any
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from contextlib import asynccontextmanager
from . import db
from models import URLModel

# Runs once at startup (https://fastapi.tiangolo.com/advanced/events/#lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_table()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/shorten", status_code=201)
def shorten_url(url: Any):
    try:
        url = URLModel(url=url)
        short_code = db.insert_url(url)
        return {"short_code": short_code}
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    