from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List, Set, Dict, Any

class Action_Type(str, Enum):
    consent_revoked = "consent revoked"
    consent_accepted = "consent accepted"
    consent_denied = "consent denied"
    authorization_granted = "authorization granted"
    data_subject_request_make_request = "data subject request: initiate"
    data_use = "data use"

class Action(BaseModel):
    type: Action_Type
    information: Dict[str, Any]

class Party(BaseModel):
    name: str
    data_controller: Set[str]  # e.g., {"consumer", "data_provider", "data_recipient"}

class Attestation(BaseModel):
    _id: int
    party: Party
    action: Action
    timestamp: datetime

class AttestationRecords(BaseModel):
    party: Party
    attestations: List[Attestation] = []
