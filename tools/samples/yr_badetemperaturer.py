# tools/yr_badetemperaturer.py — Yr bathing water temperatures
# Requires config.json: { "yr_api_key": "your-key" }

import requests
from core.db_connection import config
from core.tool_registry import mcp

_BASE_URL = "https://badetemperaturer.yr.no/api/v0"


def _headers() -> dict:
    return {"apikey": config.yr_api_key}


@mcp.tool(description="Search for Norwegian bathing spots (badeplasser) by name and return their location IDs")
def search_bathing_spots(query: str) -> list[dict]:
    response = requests.get(
        f"{_BASE_URL}/locations/searchbathingspots",
        headers=_headers(),
        params={"q": query},
        timeout=10,
    )
    response.raise_for_status()
    return [s for s in response.json() if s.get("categoryName") == "Badeplass"]


@mcp.tool(description="Get water temperature measurements for a bathing spot by its location ID. Use search_bathing_spots first to find the location ID.")
def get_bathing_temperatures(location_id: str) -> list[dict]:
    response = requests.get(
        f"{_BASE_URL}/locations/{location_id}/watertemperatures",
        headers=_headers(),
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
