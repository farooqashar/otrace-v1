from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from models.attestation_model import Action, Party, Attestation, AttestationRecords

router = APIRouter(prefix="/attestations", tags=["Attestations"])

attestation_records = {}

# POST endpoint to create a new attestation
@router.post("/attest/{party_name}/", response_model=Attestation)
def attest(party_name: str, action: Action):
    """
    Record an attestation for a specific party.
    """
    # If party doesn't exist, create it
    if party_name not in attestation_records:
        attestation_records[party_name] = AttestationRecords(party=Party(name=party_name, data_controller={"consumer"}))

    party = attestation_records[party_name]

    new_attestation = Attestation(
        _id=len(party.attestations) + 1,
        party=party.party,
        action=action,
        timestamp=datetime.now()
    )

    party.attestations.append(new_attestation)

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
def get_up_to_date_attestations(party_name: str, timestamp1: datetime, timestamp2: datetime):
    """
    Get attestations for a party that fall within the specified timestamp range.
    """
    if party_name not in attestation_records:
        raise HTTPException(status_code=404, detail="Party not found")

    party = attestation_records[party_name]
    return [
        attestation for attestation in party.attestations
        if timestamp1 <= attestation.timestamp <= timestamp2
    ]
