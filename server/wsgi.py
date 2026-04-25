from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import chat_router, file_router
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

app.include_router(chat_router, prefix="/v1")
app.include_router(file_router, prefix="/v1")
