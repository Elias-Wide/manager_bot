from sqlalchemy import (
    BOOLEAN,
    BigInteger,
    Column,
    Date,
    Integer,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Users(Base):

    telegram_id = Column(BigInteger, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    is_region_admin = Column(BOOLEAN, default=False)
    region_id = Column(ForeignKey("regions.id", ondelete="SET NULL"), nullable=True)
    ban = Column(BOOLEAN, default=False)
    office_id = Column(ForeignKey("offices.id"), nullable=False)
    region = relationship("Regions", back_populates="users", foreign_keys=[region_id])
    offices = relationship(
        "Offices",
        back_populates="managers",
    )
    work_days = relationship(
        "WorkDays",
        back_populates="user",
    )

    __table_args__ = (
        UniqueConstraint(
            "telegram_id",
            "phone_number",
            name="unique_phone_number_tg_id",
        ),
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.username})"

    def get_full_info(self):
        """
        Returns a detailed string with user information.
        """
        return (
            f"👤 {self.first_name} {self.last_name} (@{self.username})\n"
            f"Телефон: +7{self.phone_number}\n"
        )


class WorkDays(Base):
    """
    Model for tracking user workdays.
    Args:
        user_id: Telegram ID of the user.
        day: Date of the workday.
    """

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    day = Column(Date, nullable=False)
    user = relationship(Users, back_populates="work_days")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "day",
            name="unique_user_work_day",
        ),
    )
