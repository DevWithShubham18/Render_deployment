from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import log_setup

app = FastAPI(title="Report Analyzer API")


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Setup the application logging
    log_setup()

    yield


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
