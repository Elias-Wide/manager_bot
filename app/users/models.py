from sqlalchemy import (
    BOOLEAN,
    BigInteger,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Users(Base):

    telegram_id = Column(BigInteger, unique=True, nullable=False)
    phone_number = Column(Integer, nullable=False, unique=True)
    username = Column(String, nullable=False)
    manager_id = Column(BigInteger, unique=True, nullable=False)
    is_region_admin = Column(BOOLEAN, default=False) 
    ban = Column(BOOLEAN, default=False)
    point_id = Column(Integer)

    def __str__(self):
        return f"User @{self.username}"
