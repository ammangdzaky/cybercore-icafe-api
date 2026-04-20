from pydantic import BaseModel
from typing import Optional

class PCBase(BaseModel):
    pc_number: str
    pc_specs: str
    pc_type: str

class PCCreate(PCBase):
    pass

class PC(PCBase):
    id: int

    class Config:
        from_attributes = True