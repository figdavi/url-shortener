from typing import Any
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from contextlib import asynccontextmanager
from .utils import validate_url
from . import db

# Runs once at startup (https://fastapi.tiangolo.com/advanced/events/#lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_table()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/shorten", status_code=201)
def create_short_url(url: Any):
    try:
        url = validate_url(url)
        short_code = db.insert_url(url)
        return {"short_code": short_code}
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/shorten/{short_code}", status_code=200)
def get_original_url(short_code: str):
    try:
        url = db.get_url(short_code)
        return url
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))