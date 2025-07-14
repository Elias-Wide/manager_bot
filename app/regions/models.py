from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.users.models import Users  # noqa


class Regions(Base):
    """
    Model representing a region.

    Attributes:
        name (str): Name of the region.
        offices (list): List of offices (offices) in the region.
        admins (Users): Relationship to the user who is managginf the region.
    """

    name = Column(String, nullable=False, unique=True)
    offices = relationship("Offices", back_populates="region")
    admins = relationship(
        "Users", back_populates="region", foreign_keys=[Users.region_id]
    )

    def __str__(self):
        return f"{self.name}"
