from pydantic import BaseModel, HttpUrl 

class URLModel(BaseModel):
    url: HttpUrl