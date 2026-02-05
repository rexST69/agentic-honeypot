import os
from fastapi import HTTPException, Header


EXPECTED_API_KEY = os.getenv("API_KEY")
if not EXPECTED_API_KEY:
    raise RuntimeError("API_KEY environment variable is not set")


def verify_api_key(x_api_key: str = Header(...)) -> None:
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
