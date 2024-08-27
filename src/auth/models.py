import datetime

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import JSON, TIMESTAMP, Column, ForeignKey, Integer, MetaData, String, Boolean, Table

from src.database import Base

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registred_at", TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(
            Integer, primary_key=True
    )
    username: Mapped[str] = mapped_column(
            String, nullable=False
    )
    registred_at: Mapped[datetime.datetime] = mapped_column(
            TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)
    )
    role_id: Mapped[int] = mapped_column(
            Integer, ForeignKey(role.c.id)
    )
    email: Mapped[str] = mapped_column(
            String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
            String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
            Boolean, default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
            Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
            Boolean, default=False, nullable=False
    )
