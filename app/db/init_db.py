from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.session import Base, SessionLocal, engine
from app.models.media import MediaItem
from app.models.user import User


def seed_data() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        demo_user = db.scalar(select(User).where(User.username == "demo"))
        if not demo_user:
            demo_user = User(
                username="demo",
                email="demo@example.com",
                hashed_password=get_password_hash("ChangeMe123!"),
                is_active=True,
            )
            db.add(demo_user)

        existing = db.scalar(select(MediaItem).limit(1))
        if not existing:
            db.add_all(
                [
                    MediaItem(
                        external_id="arrival",
                        title="Arrival",
                        description="A cerebral first-contact story with strong atmosphere and tension.",
                        genres="sci-fi,drama,thriller",
                        maturity_rating="PG-13",
                        release_year=2016,
                    ),
                    MediaItem(
                        external_id="blade-runner-2049",
                        title="Blade Runner 2049",
                        description="A moody neo-noir sci-fi thriller focused on identity, memory, and AI.",
                        genres="sci-fi,thriller,drama",
                        maturity_rating="R",
                        release_year=2017,
                    ),
                    MediaItem(
                        external_id="the-creator",
                        title="The Creator",
                        description="A modern dystopian action drama centered on conflict around artificial intelligence.",
                        genres="sci-fi,action,thriller",
                        maturity_rating="PG-13",
                        release_year=2023,
                    ),
                    MediaItem(
                        external_id="interstellar",
                        title="Interstellar",
                        description="Epic science fiction driven by exploration, sacrifice, and emotional stakes.",
                        genres="sci-fi,adventure,drama",
                        maturity_rating="PG-13",
                        release_year=2014,
                    ),
                ]
            )
        db.commit()
    finally:
        db.close()
