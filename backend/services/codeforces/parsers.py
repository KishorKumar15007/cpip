from datetime import UTC, datetime


def parse_problem(
    problem: dict,
) -> dict:
    contest_id = problem["contestId"]
    index = problem["index"]

    return {
        "platform": "codeforces",
        "platform_problem_id": f"{contest_id}{index}",
        "title": problem["name"],
        "platform_difficulty": None,
        "cf_rating": problem.get("rating"),
        "url": (
            f"https://codeforces.com/problemset/problem/"
            f"{contest_id}/{index}"
        ),
    }


def parse_tags(
    problem: dict,
) -> list[str]:
    return problem.get("tags", [])


def parse_contest_participation(
    contest: dict,
) -> dict:
    return {
        "platform": "codeforces",
        "contest_id": str(contest["contestId"]),
        "contest_name": contest["contestName"],
        "rank": contest["rank"],
        "old_rating": contest["oldRating"],
        "new_rating": contest["newRating"],
        "participated_at": datetime.fromtimestamp(
            contest["ratingUpdateTimeSeconds"],
            tz=UTC,
        ),
    }


def parse_submission(
    submission: dict,
) -> dict:
    return {
        "platform": "codeforces",
        "platform_submission_id": str(
            submission["id"]
        ),
        "verdict": submission.get("verdict", "UNKNOWN"),
        "language": submission["programmingLanguage"],
        "submitted_at": datetime.fromtimestamp(
            submission["creationTimeSeconds"],
            tz=UTC,
        ),
    }


def parse_user(
    user: dict,
) -> dict:
    return {
        "cf_username": user["handle"],
    }
