from pydantic import BaseModel
from typing import Set, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum

class ConsentState(str, Enum):
    offered = "offered"
    accepted = "accepted"
    denied = "denied"

class User(BaseModel):
    name: str
    user_id: UUID

class Operator(BaseModel):
    name: str
    operator_id: UUID

class Data(BaseModel):
    name: str

class Operations(BaseModel):
    description: str

class Consent(BaseModel):
    consent_id: UUID
    operator: Operator
    user: User
    data: Data
    operations_permitted: Set[Operations]
    expiry_timestamp: datetime
    state: ConsentState
