from backend.db.session import SessionLocal

from backend.services.codeforces.client import (
    CodeforcesClient,
)
from backend.services.codeforces.sync import (
    CodeforcesSyncService,
)

from backend.services.leetcode.client import (
    LeetCodeClient,
)
from backend.services.leetcode.sync import (
    LeetCodeSyncService,
)

from dotenv import load_dotenv
import os

load_dotenv()

session = SessionLocal()

USER_ID = 2

try:

    print("=" * 80)
    print("CODEFORCES SYNC")
    print("=" * 80)

    cf_client = CodeforcesClient()

    cf_sync = CodeforcesSyncService(
        cf_client,
    )

    print(cf_sync.sync_all(
        session,
        USER_ID,
    ))

    print()

    print("=" * 80)
    print("LEETCODE SYNC")
    print("=" * 80)

    lc_client = LeetCodeClient(
        session_cookie=os.getenv(
            "LEETCODE_SESSION",
        ),
        csrf_token=os.getenv(
            "LEETCODE_CSRFTOKEN",
        ),
    )

    lc_sync = LeetCodeSyncService(
        lc_client,
    )

    print(lc_sync.sync_all(
        session,
        USER_ID,
    ))

finally:
    session.close()
