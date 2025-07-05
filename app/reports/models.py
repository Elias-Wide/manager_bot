from datetime import datetime
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
)

from app.core.database import Base


class Reports(Base):

    created_at = Column(DateTime, nullable=False)
    user_id = Column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    created_at_date = Column(Date, nullable=False, default=datetime.now)
    point_id = Column(ForeignKey("points.id", ondelete="CASCADE"), nullable=True)
    img = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "created_at_date",
            "point_id",
            name="unique_report_in_a_day",
        ),
    )

    def __str__(self):
        return f"Отчет прихода. Офис {self.point_id} {self.datetime}"
