from fastapi import FastAPI
from app.api import events
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)

app.include_router(events.router, prefix="/events")

@app.on_event("startup")
async def startup_event():
    try:
        await events.fetch_and_cache_events()
    except Exception as e:
        print(f"Error during startup event fetch: {e}")
