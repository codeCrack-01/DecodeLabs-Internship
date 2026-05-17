from fastapi import APIRouter

from endpoints.encrypt_data import encrypt_decrypt
from endpoints.extract_data import extract

endpoint = APIRouter(prefix="/api", tags=["endpoints"])
endpoint.include_router(extract)
endpoint.include_router(encrypt_decrypt)
