from sqlalchemy import (
    BOOLEAN,
    BigInteger,
    Column,
    DateTime,
    Integer,
    ForeignKey,
    String,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Reports(Base):

    datetime = Column(DateTime, nullable=False)
    point_id = Column(
        ForeignKey("points.id", ondelete="CASCADE"), nullable=True
    )
    img = Column(String, nullable=False)
    
    def __str__(self):
        return f"Report {self.id} office - {self.point_id} {self.datetime}"

    __table_args__ = (
        UniqueConstraint(
            "datetime",
            "point_id",
            name="unique_report_in_a_day",
        )
    )