import aioredis
import json
from datetime import datetime
from typing import List
from app.core.config import settings

# Initialize Redis client
redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

async def cache_events(events: List[dict]):
    """
    Cache events in Redis.
    """
    try:
        for event in events:
            event['starts_at'] = event['starts_at'].isoformat()
            event['ends_at'] = event['ends_at'].isoformat()
            await redis.set(f"event:{event['id']}", json.dumps(event))
    except Exception as e:
        print(f"Exception during cache events: {e}")

async def get_cached_events(starts_at: datetime, ends_at: datetime):
    """
    Get cached events from Redis within the specified date range.
    """
    try:
        keys = await redis.keys("event:*")
        events = []
        for key in keys:
            event = json.loads(await redis.get(key))
            event_start = datetime.fromisoformat(event['starts_at'])
            event_end = datetime.fromisoformat(event['ends_at'])
            if starts_at <= event_start <= ends_at or starts_at <= event_end <= ends_at:
                events.append(event)
        return events
    except Exception as e:
        print(f"Exception during get cached events: {e}")
        return []
