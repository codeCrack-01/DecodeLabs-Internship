import asyncio
from fastapi import FastAPI, HTTPException, Query
import httpx

NASA_IMAGE_API = "https://images-api.nasa.gov"
NASA_APOD_API = "https://api.nasa.gov/planetary/apod"

app = FastAPI(title="NASA Moon Middleware API", version="1.0.0")


@app.get("/")
def root():
    return {"service": "NASA Moon Middleware", "status": "running"}


@app.get("/moon/images")
async def get_moon_images(q: str = Query("moon", description="Search query"), limit: int = Query(5, ge=1, le=50)):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{NASA_IMAGE_API}/search", params={"q": q, "media_type": "image"})
        resp.raise_for_status()
        data = resp.json()

    items = data.get("collection", {}).get("items", [])[:limit]
    results = []
    for item in items:
        data_node = item.get("data", [{}])[0]
        links = item.get("links", [{}])
        results.append({
            "title": data_node.get("title"),
            "description": data_node.get("description"),
            "date_created": data_node.get("date_created"),
            "nasa_id": data_node.get("nasa_id"),
            "image_url": links[0].get("href") if links else None,
        })

    return {"query": q, "count": len(results), "results": results}


@app.get("/moon/apod")
async def get_moon_apod(api_key: str = Query("DEMO_KEY", description="NASA API key")):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{NASA_APOD_API}",
            params={"api_key": api_key, "count": 5},
        )
        resp.raise_for_status()
        items = resp.json()

    moon_items = [item for item in items if "moon" in (item.get("title", "") + item.get("explanation", "")).lower()]
    if not moon_items:
        moon_items = items[:3]

    return {
        "source": "NASA APOD",
        "count": len(moon_items),
        "results": [
            {
                "title": item.get("title"),
                "explanation": item.get("explanation"),
                "date": item.get("date"),
                "image_url": item.get("hdurl") or item.get("url"),
            }
            for item in moon_items
        ],
    }


@app.get("/moon")
async def get_moon_overview():
    async with httpx.AsyncClient() as client:
        img_resp, apod_resp = await asyncio.gather(
            client.get(f"{NASA_IMAGE_API}/search", params={"q": "moon", "media_type": "image"}),
            client.get(f"{NASA_APOD_API}", params={"api_key": "DEMO_KEY", "count": 3}),
        )
        img_resp.raise_for_status()
        apod_resp.raise_for_status()

    img_data = img_resp.json()
    apod_data = apod_resp.json()

    items = img_data.get("collection", {}).get("items", [])[:3]
    images = []
    for item in items:
        d = item.get("data", [{}])[0]
        images.append({
            "title": d.get("title"),
            "nasa_id": d.get("nasa_id"),
            "description": d.get("description"),
        })

    apod_results = [
        {
            "title": item.get("title"),
            "date": item.get("date"),
            "url": item.get("hdurl") or item.get("url"),
        }
        for item in apod_data
    ]

    return {
        "total_images": img_data.get("collection", {}).get("metadata", {}).get("total_hits", 0),
        "sample_images": images,
        "apod_entries": apod_results,
    }
