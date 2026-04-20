from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class PCStation(Base):
    __tablename__ = "pc_stations"

    id = Column(Integer, primary_key=True, index=True)
    pc_number = Column(String, unique=True, index=True)
    pc_specs = Column(String)
    pc_type = Column(String)

    sessions = relationship("UsageSession", back_populates="pc")