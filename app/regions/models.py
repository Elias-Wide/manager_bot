from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.core.database import Base
from app.core.config import settings

from app.users.models import Users  # noqa


class Regions(Base):
    """
    Model representing a region.

    Attributes:
        ceo_id (int): Foreign key to the user who is the CEO of the region.
        name (str): Name of the region.
        points (list): List of points (offices) in the region.
        ceo (Users): Relationship to the user who is the CEO.
        users (list): List of users belonging to the region.
    """

    ceo_id = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name = Column(String, nullable=False, unique=True)
    points = relationship("Points", back_populates="region")
    ceo = relationship("Users", foreign_keys=[ceo_id], backref="regions_ceo")
    users = relationship(
        "Users", back_populates="region", foreign_keys="Users.region_id"
    )

    def __str__(self):
        return f"{self.name}"
