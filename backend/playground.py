from sqlalchemy import select

from backend.db.session import SessionLocal
from backend.models.user import User


session = SessionLocal()

try:
    # -------------------------
    # INSERT
    # -------------------------

    test_user = User(
        username="orm_test_user",
        email="orm_test@example.com",
        lc_username="orm_test_lc",
        cf_username="orm_test_cf",
    )

    session.add(test_user)
    session.commit()

    print("User inserted.")

    # -------------------------
    # SELECT
    # -------------------------

    stmt = select(User).where(
        User.username == "orm_test_user"
    )

    user = session.execute(stmt).scalar_one()

    print(
        user.user_id,
        user.username,
        user.email,
    )

    # -------------------------
    # DELETE
    # -------------------------

    session.delete(user)
    session.commit()

    print("User deleted.")

    # -------------------------
    # VERIFY DELETION
    # -------------------------

    stmt = select(User).where(
        User.username == "orm_test_user"
    )

    user = session.execute(stmt).scalar_one_or_none()

    print("After deletion:", user)

finally:
    session.close()
