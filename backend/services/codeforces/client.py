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

        if not isinstance(data, dict):
            raise ValueError(
                "Invalid Codeforces API response."
            )

        if data.get("status") != "OK":
            raise ValueError(
                "Codeforces API Error: "
                f"{data.get('comment', 'Unknown error')}"
            )

        if "result" not in data:
            raise ValueError(
                "Invalid Codeforces API response: "
                "missing result."
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

        if (
            not isinstance(result, list)
            or len(result) == 0
            or not isinstance(result[0], dict)
        ):
            raise ValueError(
                "Invalid Codeforces user.info response."
            )

        return result[0]

    def get_user_rating(
        self,
        handle: str,
    ):
        result = self._get(
            "user.rating",
            {"handle": handle},
        )

        if not isinstance(result, list):
            raise ValueError(
                "Invalid Codeforces user.rating response."
            )

        return result

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

        result = self._get(
            "user.status",
            params,
        )

        if not isinstance(result, list):
            raise ValueError(
                "Invalid Codeforces user.status response."
            )

        return result

    def get_problemset(self):
        result = self._get(
            "problemset.problems"
        )

        if not isinstance(result, dict):
            raise ValueError(
                "Invalid Codeforces problemset response."
            )

        if "problems" not in result:
            raise ValueError(
                "Invalid Codeforces problemset response: "
                "missing problems."
            )

        if not isinstance(result["problems"], list):
            raise ValueError(
                "Invalid Codeforces problemset response: "
                "problems must be a list."
            )

        return result
    
    def close(self):
        self.client.close()
