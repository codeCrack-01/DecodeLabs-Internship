import hashlib
from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image
from PIL.ExifTags import TAGS

from services.extraction import extract_gps

extract = APIRouter()


@extract.post("/extract")
async def extract_metadata(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):  # type: ignore
        raise HTTPException(status_code=400, detail="File must be an image")

    content = await file.read()

    try:
        image = Image.open(BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image")

    exif_raw = image.getexif()
    exif = {}
    gps = None

    for tag_id, value in exif_raw.items():
        tag = TAGS.get(tag_id, str(tag_id))

        if tag == "GPSInfo":
            gps = extract_gps(value)
        else:
            exif[tag] = str(value)

    sha256 = hashlib.sha256(content).hexdigest()

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "image": {
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "mode": image.mode,
        },
        "file": {"size_bytes": len(content), "sha256": sha256},
        "gps": gps,
        "metadata": exif,
    }
