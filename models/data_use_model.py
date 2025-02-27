from typing import Any
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

# Enum for different reasons for data use
class Basis_Type(str, Enum):
    consent = "consent"
    legal_obligation = "legal_obligation"
    vital_interests = "vital_interests"
    public_interest = "public_interest"
    legitimate_interest = "legitimate_interest"

class Basis(BaseModel):
    base_type: Basis_Type
    basis_object: Any

class DataSubject(BaseModel):
    name: str

class Operator(BaseModel):
    name: str

class Data(BaseModel):
    description: str

class Operation(BaseModel):
    operation_type: str

class DataUse(BaseModel):
    id: UUID
    operator: Operator
    data: Data
    data_subject: DataSubject
    operation: Operation
    basis: Basis
    timestamp: datetime
