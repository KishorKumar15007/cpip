from backend.db.session import SessionLocal

from backend.services.analytics.service import (
    AnalyticsService,
)

analytics_service = AnalyticsService()

with SessionLocal() as session:

    summary = (
        analytics_service.get_user_summary(
            session,
            user_id=4,
        )
    )
    history = (
        analytics_service.get_rating_history(
            session,
            user_id=4,
        )
    )
    top_tags = (
        analytics_service.get_top_tags(
            session,
            user_id=4,
        )
    )
    rates = (
        analytics_service.get_tag_success_rates(
            session,
            user_id=4,
        )
    )
    distribution = (
        analytics_service.get_rating_distribution(
            session,
            user_id=4,
        )
    )

    for row in distribution:
        print(row)

    # for row in rates:
    #     print(row)

    # print(
    #     analytics_service.get_verdict_breakdown(
    #         session,
    #         user_id=4,
    #     )
    # )

    # print(top_tags)

    # print(history[:5])

    # print(summary)
