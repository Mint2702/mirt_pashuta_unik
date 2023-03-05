from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import Engine


from settings import settings


def create_session() -> Session:
    engine: Engine = create_engine(settings.db_url, pool_pre_ping=True)
    session_maker = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    return session_maker()


@contextmanager
def get_session():
    session: Session = create_session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
