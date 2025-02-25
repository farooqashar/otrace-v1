from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

# Enum for different reasons for data use
class Basis(str, Enum):
    consent = "consent"
    legal_obligation = "legal_obligation"
    vital_interests = "vital_interests"
    public_interest = "public_interest"
    legitimate_interest = "legitimate_interest"

class DataSubject(BaseModel):
    name: str
    data_subject_id: UUID

class Operator(BaseModel):
    name: str
    operator_id: UUID

class Data(BaseModel):
    name: str

class Operation(BaseModel):
    description: str

class DataUse(BaseModel):
    data_use_id: UUID
    operator: Operator
    data: Data
    data_subject: DataSubject
    operation: Operation
    basis: Basis
    timestamp: datetime
