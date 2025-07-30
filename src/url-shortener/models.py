from pydantic import BaseModel, HttpUrl, field_validator, ValidationError
from typing import Any

class URLModel(BaseModel):
    url: HttpUrl

    @field_validator('numbers', mode='before')
    @classmethod
    def validate_url(cls, url: Any) -> HttpUrl:
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
