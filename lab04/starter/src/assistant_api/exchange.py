import httpx
from typing import Optional


class ExternalServiceError(Exception):
    """Error raised when an error occurs while connecting to the Exchange Rates API."""
    pass


class ExchangeClient:
    def __init__(self, timeout_s: float = 3.0):
        # Public, free and key-free API
        self.url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.timeout_s = timeout_s
        self._cache: Optional[dict] = None  # Store backup data

    def current_rate(self) -> dict:
        # Habit 2: Retry (2 attempts max if failed)
        for attempt in range(2):
            try:
                # Habit 1: Timeout
                with httpx.Client(timeout=self.timeout_s) as client:
                    response = client.get(self.url)
                    response.raise_for_status()
                    data = response.json()

                    rate = data["rates"].get("VND", 25000)
                    result = {"currency": "USD to VND", "rate": rate, "stale": False}


                    self._cache = result
                    return result

            except (httpx.HTTPError, ValueError, KeyError):
                if attempt == 1:
                    break

        # Habit 3: Backup Plan
        if self._cache:
            backup = self._cache.copy()
            backup["stale"] = True
            return backup

        raise ExternalServiceError("Exchange rate service is down and no cache is available.")