from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SessionBase(BaseModel):
    start_time: datetime
    pc_id: int

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    end_time: datetime
    total_price: float

class UsageSession(SessionBase):
    id: int
    end_time: Optional[datetime] = None
    total_price: float

    class Config:
        from_attributes = True