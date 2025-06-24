import requests
from django.conf import settings

def firecrawl_search(query):
    headers = {"x-api-key": settings.FIRECRAWL_API_KEY}
    payload = {
        "query": query,
        "mode": "structured",
        "includeRaw": False,
        "includeLinks": True,
    }
    resp = requests.post("https://api.firecrawl.dev/search", json=payload, headers=headers)
    return resp.json()
