# app/models/admin_user.py

from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class AdminUser(Base):
    __tablename__ = "admin_users"

    admin_user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<AdminUser(id={self.admin_user_id}, name='{self.user_name}')>"