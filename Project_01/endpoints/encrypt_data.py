import base64
import json
import os
from datetime import datetime
from io import BytesIO
from zipfile import ZipFile

from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image

from services.encryptions import embed_data, extract_data

load_dotenv()

encrypt_decrypt = APIRouter()
MAGIC = (
    os.environ.get("MAGIC") or "D3C0D3"
)  # My Custom Flag to identify the schematic, for testing, I have left it here as default, but use dotenv files to hide it in action!


@encrypt_decrypt.post("/encrypt")
async def encrypt(file: UploadFile = File(...), message: str = Form(...)):
    if not file.content_type.startswith("image/"):  # type: ignore
        raise HTTPException(400, "File must be an image")
    content = await file.read()

    try:
        image = Image.open(BytesIO(content))
    except Exception:
        raise HTTPException(400, "Invalid image")

    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted = cipher.encrypt(message.encode())

    payload = {"magic": MAGIC, "data": base64.b64encode(encrypted).decode()}
    payload_bytes = json.dumps(payload).encode()

    try:
        encoded_image = embed_data(image, payload_bytes)
    except ValueError as e:
        raise HTTPException(400, str(e))

    image_buffer = BytesIO()

    # The PNG is good for quality, other types loose that, thats why...
    encoded_image.save(image_buffer, format="PNG")
    image_buffer.seek(0)

    key_payload = {
        "algorithm": "Fernet",
        "created_at": datetime.now().isoformat(),
        "key": key.decode(),
    }

    key_bytes = json.dumps(key_payload, indent=2).encode()

    # =====================================================
    # Create ZIP Bundle
    # =====================================================

    zip_buffer = BytesIO()

    with ZipFile(zip_buffer, "w") as zip_file:
        zip_file.writestr("encrypted.png", image_buffer.getvalue())
        zip_file.writestr("key.txt", key_bytes)

    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=encrypted_bundle.zip"},
    )


@encrypt_decrypt.post("/decrypt")
async def decrypt(file: UploadFile = File(...), key: str = Form(...)):
    content = await file.read()

    try:
        image = Image.open(BytesIO(content))
    except Exception:
        raise HTTPException(400, "Invalid image")

    raw = extract_data(image)

    try:
        start = raw.find(b'{"magic"')
        if start == -1:
            raise ValueError()
        end = raw.find(b"}", start)
        payload = json.loads(raw[start : end + 1])
    except Exception:
        raise HTTPException(400, "No hidden payload found")

    if payload.get("magic") != MAGIC:
        raise HTTPException(400, "Invalid payload")

    encrypted = base64.b64decode(payload["data"])
    try:
        cipher = Fernet(key.encode())
        decrypted = cipher.decrypt(encrypted)

    except InvalidToken:
        raise HTTPException(401, "Incorrect key or corrupted image")
    return {"message": decrypted.decode()}
