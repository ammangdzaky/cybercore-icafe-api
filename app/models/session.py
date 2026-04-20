from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.database import Base

class UsageSession(Base):
    __tablename__ = "usage_sessions"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    total_price = Column(Float, default=0.0)
    pc_id = Column(Integer, ForeignKey("pc_stations.id"))

    pc = relationship("PCStation", back_populates="sessions")