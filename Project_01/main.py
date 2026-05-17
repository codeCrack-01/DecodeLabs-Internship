from fastapi import FastAPI

from endpoints import endpoint

app = FastAPI(title="HackerJr API", version="1.0.0")
app.include_router(endpoint)


@app.get("/")
def root():
    return {"service": "exploit image metadata", "status": "running"}
