from datetime import datetime, UTC

def parse_problem(
    problem: dict,
) -> dict:

    return {
        "platform": "leetcode",
        "platform_problem_id": str(
            problem["id"]
        ),
        "title": problem["title"],
        "platform_difficulty": (
            problem["difficulty"]
            .lower()
        ),
        "url": (
            "https://leetcode.com/problems/"
            f"{problem['titleSlug']}/"
        ),
        "tags": [
            tag["name"]
            for tag in problem["topicTags"]
        ],
    }

def parse_submission(
    submission: dict,
) -> dict:

    return {
        "platform": "leetcode",
        "platform_submission_id": str(
            submission["id"]
        ),
        "problem_slug": submission[
            "titleSlug"
        ],
        "verdict": submission[
            "statusDisplay"
        ],
        "language": submission[
            "lang"
        ],
        "submitted_at": datetime.fromtimestamp(
            int(submission["timestamp"]),
            tz=UTC,
        ),
    }

def parse_user(
    user: dict,
) -> dict:

    return {
        "lc_username": user[
            "matchedUser"
        ]["username"],
    }
