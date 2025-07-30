from pydantic import ValidationError
from typing import Any
from .models import URLModel


def validate_url(url: Any) -> URLModel:
    """Validates the given URL and returns a URLModel instance

    Args:
        url (Any): The url to validate.

    Raises:
        last_err: The last ValidationError, if any, for the url.
        ValueError: Unexpected validation error.

    Returns:
        URLModel: Constructed and validated URLModel
    """
    candidates: list[Any] = [url, f"https://{url}", f"https://www.{url}"]
    last_err = None

    for candidate in candidates:
        try:
            validated = URLModel(url=candidate)
            return validated
        except ValidationError as e:
            # Store error, but continue trying all candidates, in case one works
            last_err = e

    # If all canditates fail:
    if last_err:
        raise last_err
    else:
        raise ValueError("Unexpected url validation error.")

