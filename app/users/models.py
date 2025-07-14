from sqlalchemy import (
    BOOLEAN,
    BigInteger,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Users(Base):
    """
    Model representing a user in the system.

    Attributes:
        telegram_id (int): Unique Telegram user ID.
        first_name (str): User's first name.
        last_name (str): User's last name (optional).
        phone_number (str): User's phone number (unique).
        username (str): Telegram username.
        ban (bool): Whether the user is banned.
        office_id (int): Foreign key to the user's office.
        offices (Offices): Relationship to the Offices model (managed offices).
        work_days (list[WorkDays]): Relationship to the user's workdays.

    Table constraints:
        - Unique constraint on (telegram_id, phone_number).

    Methods:
        __str__: Returns a string representation of the user.
        get_full_info: Returns a detailed string with user information.
    """

    telegram_id = Column(BigInteger, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    ban = Column(BOOLEAN, default=False)
    office_id = Column(ForeignKey("offices.id"), nullable=False)
    region_id = Column(
        ForeignKey("regions.id", ondelete="SET NULL"), nullable=True
    )
    region =  relationship(
        "Regions",
        back_populates="admins",
    )
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
    Model for tracking user working days.
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
