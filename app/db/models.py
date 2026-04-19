from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from datetime import datetime, timezone

from app.db.base import Base

class User(Base):
	"""Модель пользователя"""

	__tablename__ = "users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
	password_hash: Mapped[str] = mapped_column(String(100), nullable=False)
	role: Mapped[str] = mapped_column(String(50), nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

	messages: Mapped[list["ChatMessage"]] = relationship(back_populates="user")

class ChatMessage(Base):
	"""Модель сообщения чата"""
	__tablename__ = "messages"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
	role: Mapped[str] = mapped_column(String(50), nullable=False)
	content: Mapped[str] = mapped_column(Text, nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

	user: Mapped["User"] = relationship(back_populates="messages")

