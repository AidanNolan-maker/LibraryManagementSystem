import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.database import Base
from app.database import models

@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
    )

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

    engine.dispose()