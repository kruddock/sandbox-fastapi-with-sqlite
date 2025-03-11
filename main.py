from contextlib import asynccontextmanager

from fastapi import FastAPI

from routes.album import router as album_routes
from routes.team import router as team_routes

from db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def up() -> dict[str, str]:
    return { "status": "Api is running" }

app.include_router(album_routes)
app.include_router(team_routes)
