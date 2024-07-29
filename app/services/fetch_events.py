import aiohttp
import xmltodict
from datetime import datetime
from app.services.cache import cache_events
from app.core.config import settings

async def fetch_and_cache_events():
    """
    Fetch events from the external provider and cache them.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(settings.PROVIDER_URL) as response:
                if response.status == 200:
                    xml_data = await response.text()
                    events_dict = xmltodict.parse(xml_data)
                    events = process_events(events_dict)
                    await cache_events(events)
                else:
                    print(f"Error fetching data from provider: HTTP {response.status}")
    except Exception as e:
        print(f"Exception during fetch and cache: {e}")

def process_events(events_dict):
    """
    Process the XML data and return a list of event dictionaries.
    """
    try:
        events = []

        if 'eventList' not in events_dict or 'output' not in events_dict['eventList'] or 'base_event' not in events_dict['eventList']['output']:
            print("Key 'eventList' or 'output' or 'base_event' not found in the response.")
            return events
        
        base_events = events_dict['eventList']['output']['base_event']
        if isinstance(base_events, dict):
            base_events = [base_events]  # Ensure it's a list

        for base_event in base_events:
            if base_event['@sell_mode'] == 'online':
                event = base_event['event']
                zones = event['zone']
                if isinstance(zones, dict):
                    zones = [zones]  # Ensure zones is a list

                events.append({
                    'id': int(event['@event_id']),
                    'name': base_event['@title'],
                    'starts_at': datetime.fromisoformat(event['@event_start_date']),
                    'ends_at': datetime.fromisoformat(event['@event_end_date']),
                    'zones': [
                        {
                            'zone_id': zone['@zone_id'],
                            'capacity': zone['@capacity'],
                            'price': zone['@price'],
                            'name': zone['@name'],
                            'numbered': "true" if zone['@numbered'] == 'true' else "false"
                        } for zone in zones
                    ]
                })
        return events
    except Exception as e:
        print(f"Exception during process events: {e}")
        return []
