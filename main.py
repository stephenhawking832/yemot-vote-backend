# main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title="Voting System API",
    openapi_url="/api/v1/openapi.json"
)


# For development, this is your Vue dev server.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://vote.hapitron.online", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True, # Allows cookies to be included in requests
    allow_methods=["*"],    # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)
# Include the main router with a global prefix
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Voting API"}