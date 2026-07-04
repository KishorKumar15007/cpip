import httpx


class LeetCodeClient:
    BASE_URL = "https://leetcode.com/graphql"

    def __init__(
        self,
        timeout: int = 10,
        session_cookie: str | None = None,
        csrf_token: str | None = None,
    ):
        headers = {}
        cookies = {}

        self.is_authenticated = (
            session_cookie is not None
            and csrf_token is not None
        )

        if self.is_authenticated:
            headers["x-csrftoken"] = csrf_token

            cookies["LEETCODE_SESSION"] = session_cookie
            cookies["csrftoken"] = csrf_token

        self.client = httpx.Client(
            timeout=timeout,
            headers=headers,
            cookies=cookies,
        )

    def _require_authentication(
        self,
    ):
        if not self.is_authenticated:
            raise ValueError(
                "This operation requires an authenticated LeetCode session."
            )

    def _graphql(
        self,
        query: str,
        variables: dict | None = None,
        operation_name: str | None = None,
    ) -> dict:

        payload = {
            "query": query,
            "variables": variables or {},
        }

        if operation_name is not None:
            payload["operationName"] = operation_name

        response = self.client.post(
            self.BASE_URL,
            json=payload,
        )

        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            raise ValueError(
                f"LeetCode GraphQL Error: {data['errors']}"
            )

        return data["data"]

    def get_user_profile(
        self,
        username: str,
    ) -> dict:

        query = """
        query getUserProfile($username: String!) {
          matchedUser(username: $username) {
            username
          }
        }
        """

        return self._graphql(
            query=query,
            variables={
                "username": username,
            },
            operation_name="getUserProfile",
        )

    def get_submission_list(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> dict:

        self._require_authentication()

        query = """
        query submissions(
          $offset: Int!
          $limit: Int!
          $lastKey: String
          $questionSlug: String
        ) {
          submissionList(
            offset: $offset
            limit: $limit
            lastKey: $lastKey
            questionSlug: $questionSlug
          ) {
            hasNext
            submissions {
              id
              titleSlug
              statusDisplay
              lang
              timestamp
            }
          }
        }
        """

        return self._graphql(
            query=query,
            variables={
                "offset": offset,
                "limit": limit,
                "lastKey": None,
                "questionSlug": None,
            },
            operation_name="submissions",
        )

    def get_problemset(
        self,
        offset: int = 0,
        limit: int = 100,
    ) -> dict:

        query = """
        query problemsetQuestionListV2(
          $filters: QuestionFilterInput
          $limit: Int
          $searchKeyword: String
          $skip: Int
          $sortBy: QuestionSortByInput
          $categorySlug: String
        ) {
          problemsetQuestionListV2(
            filters: $filters
            limit: $limit
            searchKeyword: $searchKeyword
            skip: $skip
            sortBy: $sortBy
            categorySlug: $categorySlug
          ) {
            questions {
              id
              title
              titleSlug
              difficulty
              topicTags {
                name
              }
            }
            hasMore
          }
        }
        """

        return self._graphql(
            query=query,
            variables={
                "skip": offset,
                "limit": limit,
                "categorySlug": "all-code-essentials",
                "searchKeyword": "",
                "filters": {
                    "filterCombineType": "ALL",
                    "statusFilter": {
                        "questionStatuses": [],
                        "operator": "IS",
                    },
                    "difficultyFilter": {
                        "difficulties": [],
                        "operator": "IS",
                    },
                    "languageFilter": {
                        "languageSlugs": [],
                        "operator": "IS",
                    },
                    "topicFilter": {
                        "topicSlugs": [],
                        "operator": "IS",
                    },
                    "acceptanceFilter": {},
                    "frequencyFilter": {},
                    "frontendIdFilter": {},
                    "lastSubmittedFilter": {},
                    "publishedFilter": {},
                    "companyFilter": {
                        "companySlugs": [],
                        "operator": "IS",
                    },
                    "positionFilter": {
                        "positionSlugs": [],
                        "operator": "IS",
                    },
                    "positionLevelFilter": {
                        "positionLevelSlugs": [],
                        "operator": "IS",
                    },
                    "contestPointFilter": {
                        "contestPoints": [],
                        "operator": "IS",
                    },
                    "premiumFilter": {
                        "premiumStatus": [],
                        "operator": "IS",
                    },
                },
                "sortBy": {
                    "sortField": "CUSTOM",
                    "sortOrder": "ASCENDING",
                },
            },
            operation_name="problemsetQuestionListV2",
        )
