from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import UUID
from enum import Enum

class ConsentState(str, Enum):
    offered = "offered"
    accepted = "accepted"
    denied = "denied"
    revoked = "revoked"

class User(BaseModel):
    name: str

class Operator(BaseModel):
    name: str

class Data(BaseModel):
    description: str

class Operation(BaseModel):
    operation_type: str

class Consent(BaseModel):
    id: UUID
    operator: Operator
    user: User
    data: Data
    operations_permitted: List[Operation]
    expiry_timestamp: datetime
    state: ConsentState
