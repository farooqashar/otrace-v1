from fastapi import APIRouter, HTTPException
from typing import List, Set
from datetime import datetime
from uuid import UUID, uuid4
from models.consent_model import Consent, User, Operator, Data, Operations, ConsentState

router = APIRouter(prefix="/consents", tags=["Consents"])

consents_offered = {}
consents_accepted = {}
consents_denied = {}

# POST endpoint to offer a consent
@router.post("/offer/", response_model=Consent)
def offer_consent(operator: Operator, user: User, data: Data, operations: Set[Operations], expiry_timestamp: datetime):
    """
    Operator offers consent to the user for using certain data for certain operations until the expiry time.
    """
    consent_id = uuid4()
    consent = Consent(
        consent_id=consent_id,
        operator=operator,
        user=user,
        data=data,
        operations_permitted=operations,
        expiry_timestamp=expiry_timestamp,
        state=ConsentState.offered,
    )

    consents_offered[consent_id] = consent
    return consent

# POST endpoint to accept a consent
@router.post("/accept/{consent_id}/")
def accept_consent(consent_id: UUID, user: User):
    """
    User accepts an offered consent.
    """
    if consent_id not in consents_offered:
        raise HTTPException(status_code=404, detail="Consent not found in offered list")

    consent = consents_offered[consent_id]
    if consent.user != user:
        raise HTTPException(status_code=400, detail="User does not match the consent")

    consent.state = ConsentState.accepted
    consents_accepted[consent_id] = consent
    del consents_offered[consent_id]
    return consent

# POST endpoint to deny a consent
@router.post("/deny/{consent_id}/")
def deny_consent(consent_id: UUID, user: User):
    """
    User denies an offered consent.
    """
    if consent_id not in consents_offered:
        raise HTTPException(status_code=404, detail="Consent not found in offered list")

    consent = consents_offered[consent_id]
    if consent.user != user:
        raise HTTPException(status_code=400, detail="User does not match the consent")

    consent.state = ConsentState.denied
    consents_denied[consent_id] = consent
    del consents_offered[consent_id]
    return consent

# POST endpoint to revoke a consent
@router.post("/revoke/{consent_id}/")
def revoke_consent(consent_id: UUID, user: User):
    """
    User revokes a consent, moving it from accepted to denied.
    """
    if consent_id not in consents_accepted:
        raise HTTPException(status_code=404, detail="Consent not found in accepted list")

    consent = consents_accepted[consent_id]
    if consent.user != user:
        raise HTTPException(status_code=400, detail="User does not match the consent")

    consent.state = ConsentState.denied
    consents_denied[consent_id] = consent
    del consents_accepted[consent_id]
    return consent

# GET endpoint to get a consent by ID
@router.get("/{consent_id}/", response_model=Consent)
def get_consent(consent_id: UUID):
    """
    Get a consent object by its ID.
    """
    if consent_id in consents_offered:
        return consents_offered[consent_id]
    elif consent_id in consents_accepted:
        return consents_accepted[consent_id]
    elif consent_id in consents_denied:
        return consents_denied[consent_id]

    raise HTTPException(status_code=404, detail="Consent not found")

# GET endpoint to list all consents for a user
@router.get("/list/{user_id}/", response_model=List[Consent])
def list_user_consents(user_id: UUID):
    """
    List all offered, accepted, and denied consents for a user.
    """
    user_consents = []

    # Check all consent states for the user
    for consent in consents_offered.values():
        if consent.user.user_id == user_id:
            user_consents.append(consent)
    for consent in consents_accepted.values():
        if consent.user.user_id == user_id:
            user_consents.append(consent)
    for consent in consents_denied.values():
        if consent.user.user_id == user_id:
            user_consents.append(consent)

    return user_consents
