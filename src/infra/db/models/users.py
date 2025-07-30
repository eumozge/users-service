from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from domain.users import value_objects
from infra.db.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[value_objects.UserId] = mapped_column(
        sa.UUID,
        primary_key=True,
        default=uuid4,
    )
    username: Mapped[value_objects.Username] = mapped_column(sa.String, unique=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=sa.sql.func.now())
