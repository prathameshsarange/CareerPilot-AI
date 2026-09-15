import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def lookup_salary(role: str, location: str = "us") -> dict:
    """Return live salary aggregates from Adzuna, or an explicit unavailable result."""
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        return {
            "status": "unavailable",
            "reason": "ADZUNA_APP_ID and ADZUNA_APP_KEY are not configured.",
            "source": "Adzuna",
        }

    requested_location = (location or "us").strip()
    country = requested_location.lower().replace("_", "-")
    search_location = ""
    if len(country) != 2:
        country = "us"
        search_location = requested_location
    query = urlencode({
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": 50,
        "what": role,
        "where": search_location,
        "content-type": "application/json",
    })
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1?{query}"

    try:
        request = Request(url, headers={"User-Agent": "CareerPilot-AI/1.0"})
        with urlopen(request, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as error:
        return {
            "status": "unavailable",
            "reason": f"Salary provider request failed: {error}",
            "source": "Adzuna",
        }

    jobs = [
        job for job in payload.get("results", [])
        if job.get("salary_min") is not None or job.get("salary_max") is not None
    ]
    if not jobs:
        return {
            "status": "unavailable",
            "reason": "No salary-bearing job listings matched the requested role.",
            "source": "Adzuna",
        }

    minimums = [job["salary_min"] for job in jobs if job.get("salary_min") is not None]
    maximums = [job["salary_max"] for job in jobs if job.get("salary_max") is not None]
    return {
        "status": "ok",
        "source": "Adzuna",
        "role": role,
        "location": location,
        "sample_size": len(jobs),
        "salary_min": round(sum(minimums) / len(minimums)) if minimums else None,
        "salary_max": round(sum(maximums) / len(maximums)) if maximums else None,
        "currency": "USD" if country == "us" else "local currency",
    }