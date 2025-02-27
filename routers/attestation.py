from uuid import uuid4
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from models.attestation_model import Action, Party, Attestation, AttestationRecords

router = APIRouter(prefix="/attestations", tags=["Attestations"])

attestation_records = {}

# POST endpoint to create a new attestation
@router.post("/attest/{party_name}/{data_controller}/", response_model=Attestation)
def attest(party_name: str, data_controller: str, action: Action):
    """
    Record an attestation for a specific party.
    """
    # If party doesn't exist, create it
    if party_name not in attestation_records:
        attestation_records[party_name] = AttestationRecords(party=Party(name=party_name, data_controller=data_controller))

    party_attestations_records = attestation_records[party_name]

    new_attestation = Attestation(
        _id=uuid4(),
        party=party_attestations_records.party,
        action=action,
        timestamp=datetime.now()
    )

    party_attestations_records.attestations.append(new_attestation)

    return new_attestation

# GET endpoint to get all attestations of a party
@router.get("/{party_name}/all/", response_model=List[Attestation])
def get_all_attestations(party_name: str):
    """
    Get all attestations for a specific party.
    """
    if party_name not in attestation_records:
        raise HTTPException(status_code=404, detail="Party not found")

    return attestation_records[party_name].attestations

# GET endpoint to get attestations within a timestamp range
@router.get("/{party_name}/up_to_date/", response_model=List[Attestation])
def get_up_to_date_attestations(party_name: str, start_time: datetime, end_time: datetime):
    """
    Get attestations for a party that fall within the specified timestamp range.
    """
    if party_name not in attestation_records:
        raise HTTPException(status_code=404, detail="Party not found")

    party_attestation_records = attestation_records[party_name]
    return [
        attestation for attestation in party_attestation_records.attestations
        if start_time <= attestation.timestamp <= end_time
    ]
