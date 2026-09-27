import httpx

from app.services.ingestion.base import LeadSource

PLACES_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"

_FIELD_MASK = (
    "places.id,places.displayName,places.formattedAddress,"
    "places.internationalPhoneNumber,places.websiteUri,places.rating"
)


class GooglePlacesSource(LeadSource):
    """Recolhe negócios HORECA através da Google Places API (New)."""

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    async def search(self, region: str, business_types: list[str]) -> list[dict]:
        results: list[dict] = []
        async with httpx.AsyncClient(timeout=10) as client:
            for business_type in business_types:
                response = await client.post(
                    PLACES_SEARCH_URL,
                    headers={
                        "X-Goog-Api-Key": self._api_key,
                        "X-Goog-FieldMask": _FIELD_MASK,
                        "Content-Type": "application/json",
                    },
                    json={"textQuery": f"{business_type} em {region}"},
                )
                response.raise_for_status()
                for place in response.json().get("places", []):
                    results.append(
                        {
                            "place_id": place.get("id"),
                            "name": place.get("displayName", {}).get("text", ""),
                            "business_type": business_type,
                            "address": place.get("formattedAddress"),
                            "phone": place.get("internationalPhoneNumber"),
                            "website": place.get("websiteUri"),
                            "rating": place.get("rating"),
                        }
                    )
        return results
