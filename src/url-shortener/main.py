import secrets
from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl, ValidationError
from contextlib import asynccontextmanager
from . import db

# Runs once at startup (https://fastapi.tiangolo.com/advanced/events/#lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_table()
    yield

app = FastAPI(lifespan=lifespan)


class URLModel(BaseModel):
    url: HttpUrl


def validate_url(url: Any) -> HttpUrl:
    """Validates the given URL and returns a HttpUrl

    Args:
        url (Any): The url to validate.

    Raises:
        last_err: The last ValidationError, if any, for the url.
        ValueError: Unexpected validation error.

    Returns:
        HttpUrl: url attribute of class pydantic.HttpUrl
    """
    candidates: list[Any] = [url, f"https://{url}", f"https://www.{url}"]
    last_err = None

    for candidate in candidates:
        try:
            validated = URLModel(url=candidate)
            return validated.url
        except ValidationError as e:
            # Store error, but continue trying all candidates, in case one works
            last_err = e

    # If all canditates fail:
    if last_err:
        raise last_err
    else:
        raise ValueError("Unexpected url validation error.")


def generate_code() -> str:
    """Generates a random URL-safe 4 byte string

    Returns:
        str: The random string
    """
    return secrets.token_urlsafe(4)


@app.post("/shorten")
def shorten_url(url: Any):
    url = validate_url(url)
    short_code = generate_code()

    db.insert_url(url, short_code)

    return f"Generated shorten url: {short_code}"
