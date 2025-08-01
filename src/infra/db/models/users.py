from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from domain.users import entities, value_objects
from infra.db.models.base import BaseModel, mapper_registry
from sqlalchemy.orm import Mapped, composite, mapped_column


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[value_objects.UserId] = mapped_column(
        sa.UUID,
        primary_key=True,
        default=uuid4,
    )
    username: Mapped[value_objects.Username] = mapped_column(sa.String, unique=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=sa.sql.func.now())


USERS_TABLE = UserModel.__table__


mapper_registry.map_imperatively(
    entities.User,
    USERS_TABLE,
    properties={
        "id": composite(value_objects.UserId, USERS_TABLE.c.id),
        "username": composite(value_objects.Username, USERS_TABLE.c.username),
    },
    column_prefix="_",
)
