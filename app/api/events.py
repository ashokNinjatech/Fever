from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from app.models.event import Event
from app.services.fetch_events import fetch_and_cache_events
from app.services.cache import get_cached_events

router = APIRouter()

@router.get("/", response_model=List[Event])
async def get_events(
    starts_at: datetime = Query(..., description="Start date-time for filtering events"),
    ends_at: datetime = Query(..., description="End date-time for filtering events")
):
    """
    Get events within the specified date range.
    """
    try:
        events = await get_cached_events(starts_at, ends_at)
        if not events:
            raise HTTPException(status_code=404, detail="No events found")
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
