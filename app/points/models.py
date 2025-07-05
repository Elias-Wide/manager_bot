from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from app.core.database import Base
from app.points.constants import WORKING_SCHEDULE
from app.regions.models import Regions  # noqa


class Points(Base):
    """Модель офиса.

    Args:
        id: id офиса в системе вб
        addres: полный адрес
        trades: созданные модели обмена кодами
        managers: менеджеры офиса
    """

    addres = Column(String, nullable=False)
    region_id = Column(ForeignKey("regions.id", ondelete="SET NULL"), nullable=True)
    working_schedule = Column(ChoiceType(WORKING_SCHEDULE), default="middle")
    region = relationship("Regions", back_populates="points")
    managers = relationship("Users", back_populates="points")

    def __str__(self):
        return f"{self.addres}"

    def get_full_info(self):
        return (
            f"Офис 📌{self.addres} id {self.id}\n"
            f"Режим работы {self.working_schedule}\n\n"
        )
