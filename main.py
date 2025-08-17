# main.py

from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title="Voting System API",
    openapi_url="/api/v1/openapi.json"
)

# Include the main router with a global prefix
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Voting API"}