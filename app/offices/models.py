from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from app.core.database import Base
from app.offices.constants import WORKING_SCHEDULE
from app.regions.models import Regions  # noqa


class Offices(Base):
    """Office_Model.

    Args:
        id: office it in wb system
        addres: current addres of the office
        region_id: id of the office workin region (disctrict)
        working_schedule: office working schedule(8-22hrs or 9-21hrs)
        managers: users that work in that office
    """

    addres = Column(String, nullable=False)
    region_id = Column(ForeignKey("regions.id", ondelete="SET NULL"), nullable=True)
    working_schedule = Column(ChoiceType(WORKING_SCHEDULE), default="middle")
    region = relationship("Regions", back_populates="offices")
    managers = relationship("Users", back_populates="offices")

    def __str__(self):
        return f"{self.addres}"

    def get_full_info(self):
        return (
            f"Офис 📌{self.addres} id {self.id}\n"
            f"Режим работы {self.working_schedule}\n\n"
        )
