from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from app.core.database import Base
from app.core.config import settings
from app.points.constants import WORKING_SCHEDULE


def same_as(column_name):
    def default_function(context):
        return context.current_parameters.get(column_name)

    return default_function


class Points(Base):
    """Модель офиса.

    Args:
        id: id офиса в системе вб
        addres: полный адрес
        trades: созданные модели обмена кодами
        managers: менеджеры офиса
    """

    id = Column(Integer, nullable=False, unique=True)
    addres = Column(String, nullable=False)
    region_id = Column(ForeignKey("regions.id", ondelete="SET NULL"), nullable=True)
    working_schedule = Column(ChoiceType(WORKING_SCHEDULE), default="middle")
    name = Column(String, nullable=True, default=same_as("addres"))
    region = relationship("Regions", back_populates="points")
    managers = relationship("Users", back_populates="points")

    def __str__(self):
        return f"{self.addres}"
