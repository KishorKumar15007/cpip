import httpx


class CodeforcesClient:
    BASE_URL = "https://codeforces.com/api"

    def __init__(self, timeout: int = 120):
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=timeout,
        )

    def _get(
        self,
        endpoint: str,
        params: dict | None = None,
    ):
        response = self.client.get(
            endpoint,
            params=params,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != "OK":
            raise ValueError(
                f"Codeforces API Error: {data.get('comment', 'Unknown error')}"
            )

        return data["result"]

    def get_user_info(
        self,
        handle: str,
    ):
        result = self._get(
            "user.info",
            {"handles": handle},
        )

        return result[0]

    def get_user_rating(
        self,
        handle: str,
    ):
        return self._get(
            "user.rating",
            {"handle": handle},
        )

    def get_user_submissions(
        self,
        handle: str,
        count: int | None = None,
    ):
        params = {
            "handle": handle,
        }

        if count is not None:
            params["count"] = count

        return self._get(
            "user.status",
            params,
        )

    def get_problemset(self):
        return self._get(
            "problemset.problems"
        )
