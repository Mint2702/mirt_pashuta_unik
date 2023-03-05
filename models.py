from sqlalchemy import (
    BigInteger,
    Column,
    Text,
    Boolean,
    Float,
    ForeignKey,
    PrimaryKeyConstraint,
    DateTime,
    MetaData,
)
from datetime import datetime
from sqlalchemy.orm import relationship, Session, as_declarative, declared_attr


metadata = MetaData()


@as_declarative(metadata=metadata)
class Base:
    created_at = Column(DateTime(timezone=False), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=False),
        onupdate=datetime.utcnow,
        default=datetime.utcnow,
    )

    def create(self, session: Session):
        session.add(self)
        session.commit()
        session.refresh(self)
        return self

    @declared_attr
    def __tablename__(cls):
        return str(cls.__name__).lower() + "s"

    _secret_columns = []  # for as_dict method

    def as_dict(self):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in self._secret_columns
        }


class User(Base):
    __tablename__ = "users"

    id: str = Column(Text(), primary_key=True)

    fio: str = Column(Text(), nullable=False)
    user_facts: str = Column(Text(), nullable=False)
    user_description: str = Column(Text(), nullable=False)

    photo_url: str = Column(Text(), unique=True, nullable=False)
    profile_description: str = Column(Text(), unique=True, nullable=False)
