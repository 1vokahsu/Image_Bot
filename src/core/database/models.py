import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped

from core.database.database import Base
from typing import Annotated, Optional

intpk = Annotated[int, mapped_column(primary_key=True)]


class UsersORM(Base):

    __tablename__ = "users"

    id: Mapped[intpk]
    user_id: Mapped[Optional[int]] = mapped_column(sa.BIGINT, unique=True)
    username: Mapped[Optional[str]]
    gens: Mapped[Optional[int]]
    age: Mapped[Optional[str]]
    sex: Mapped[Optional[str]]
    profession: Mapped[Optional[str]]
    rate: Mapped[Optional[bool]]



