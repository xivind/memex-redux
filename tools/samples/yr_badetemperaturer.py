# tools/yr_badetemperaturer.py — Yr bathing water temperatures
# Requires config.json:
#   "api_domains": { "Yr Badetemperaturer": "https://badetemperaturer.yr.no/api/v0" }
#   "api_keys": { "Yr Badetemperaturer": "your-key" }

from core.db_connection import config
from core.http_connector import HttpConnector
from core.tool_registry import mcp

_SERVICE = "Yr Badetemperaturer"
connector = HttpConnector(config.api_domains[_SERVICE])
_headers = {"apikey": config.api_keys[_SERVICE]}


@mcp.tool(description="Search for Norwegian bathing spots (badeplasser) by name and return their location IDs")
def search_bathing_spots(query: str) -> list[dict]:
    results = connector.get(
        "/locations/searchbathingspots",
        headers=_headers,
        params={"q": query},
        timeout=10,
    )
    return [s for s in results if s.get("categoryName") == "Badeplass"]


@mcp.tool(description="Get water temperature measurements for a bathing spot by its location ID. Use search_bathing_spots first to find the location ID.")
def get_bathing_temperatures(location_id: str) -> list[dict]:
    return connector.get(
        f"/locations/{location_id}/watertemperatures",
        headers=_headers,
        timeout=10,
    )
