from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from fastapi import status
from pydantic import BaseModel
from typing import Optional
import logging
import time
from logging import Logger

# Define the user model
class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str
    height: float
    notes: Optional[str]

# Define the logger
logger = logging.getLogger(__name__)

# Initialize the in-memory storage
in_memory_storage = []

# Create the FastAPI application
app = FastAPI()

# Add CORS middleware
origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logger middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request to {request.url} took {process_time:.2f} seconds")
    return response

# Define the endpoint to create a user
@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    in_memory_storage.append(user)
    return user