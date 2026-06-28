from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    status,
)
from sqlalchemy.orm import Session

from backend.api.dependencies import (
    get_session,
)
from backend.services.analytics.service import (
    AnalyticsService,
)

from backend.schemas.analytics import (
    UserSummaryResponse,
    RatingHistoryEntry,
    TopTagResponse,
    VerdictBreakdownResponse,
    TagSuccessRateResponse,
    RatingDistributionResponse
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

analytics_service = AnalyticsService()

UserId = Annotated[
    int,
    Path(
        gt=0,
        description="Internal CPIP user ID.",
    ),
]

DBSession = Annotated[
    Session,
    Depends(get_session),
]


@router.get(
    "/users/{user_id}/summary",
    summary="Get user summary",
    description="Returns overall submission and rating statistics for a user.",
    response_model=UserSummaryResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "description": "User not found.",
        },
    },
)
def get_user_summary(
    user_id: UserId,
    session: DBSession,
):
    return analytics_service.get_user_summary(
        session,
        user_id,
    )


@router.get(
    "/users/{user_id}/rating-history",
    summary="Get rating history",
    description="Returns the user's Codeforces rating progression over time.",
    response_model=list[RatingHistoryEntry],
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "description": "User not found.",
        },
    },
)
def get_rating_history(
    user_id: UserId,
    session: DBSession,
):
    return analytics_service.get_rating_history(
        session,
        user_id,
    )


@router.get(
    "/users/{user_id}/top-tags",
    summary="Get top solved tags",
    description="Returns the user's most solved Codeforces tags.",
    response_model=list[TopTagResponse],
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "description": "User not found.",
        },
    },
)
def get_top_tags(
    user_id: UserId,
    session: DBSession,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=50,
            description="Maximum number of tags to return.",
        ),
    ] = 10,
):
    return analytics_service.get_top_tags(
        session,
        user_id,
        limit,
    )


@router.get(
    "/users/{user_id}/verdict-breakdown",
    summary="Get verdict breakdown",
    description="Returns the distribution of submission verdicts.",
    response_model=list[VerdictBreakdownResponse],
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "description": "User not found.",
        },
    },
)
def get_verdict_breakdown(
    user_id: UserId,
    session: DBSession,
):
    return analytics_service.get_verdict_breakdown(
        session,
        user_id,
    )


@router.get(
    "/users/{user_id}/tag-success-rates",
    summary="Get tag success rates",
    description="Returns success statistics for each Codeforces tag.",
    response_model=list[TagSuccessRateResponse],
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "description": "User not found.",
        },
    },
)
def get_tag_success_rates(
    user_id: UserId,
    session: DBSession,
):
    return analytics_service.get_tag_success_rates(
        session,
        user_id,
    )


@router.get(
    "/users/{user_id}/rating-distribution",
    summary="Get solved problem rating distribution",
    description="Returns the number of solved problems at each Codeforces rating.",
    response_model=list[RatingDistributionResponse],
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "description": "User not found.",
        },
    },
)
def get_rating_distribution(
    user_id: UserId,
    session: DBSession,
):
    return analytics_service.get_rating_distribution(
        session,
        user_id,
    )
