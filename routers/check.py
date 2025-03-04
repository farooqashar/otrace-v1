from fastapi import APIRouter, HTTPException
from datetime import datetime
from models.consent_model import ConsentState
from firebase import db

router = APIRouter(prefix="/check", tags=["Check"])

@router.get("/{attestation_id}/{consent_id}")
def check_attestation_validity(attestation_id: str, consent_id: str):
    """
    Checks whether an attestation (data use) is valid under a given consent (basis).
    Returns True with the valid time range if it is valid, or False otherwise.
    """
    # Retrieve attestation
    attestation_doc = db.collection("attestations").document(attestation_id).get()
    if not attestation_doc.exists:
        raise HTTPException(status_code=404, detail="Attestation not found")

    attestation = attestation_doc.to_dict()

    # Retrieve consent (basis)
    consent_doc = db.collection("consents").document(consent_id).get()
    if not consent_doc.exists:
        raise HTTPException(status_code=404, detail="Consent not found")

    consent = consent_doc.to_dict()

    # Compare consent expiry timestamp as string
    consent_expiry_str = consent["expiry_timestamp"].strftime('%Y-%m-%dT%H:%M:%SZ')  # ISO 8601 format
    current_time_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    # Ensure the consent is accepted and not expired
    if consent["state"] != ConsentState.accepted.value or consent_expiry_str < current_time_str:
        return {"valid": False, "message": "Consent is not active or has expired."}

    # Validate if attestation matches consent
    attestation_action = attestation["action"]
    consent_operations = [op["operation_type"] for op in consent["operations_permitted"]]

    if (
        attestation["party"]["name"] == consent["operator"]["name"]
        and attestation_action["type"] == "data use"
        and attestation_action["information"].get("data") == consent["data"]["description"]
        and attestation_action["information"].get("operation") in consent_operations
    ):
        return {
            "valid": True,
            "allowed_time_range": {"start": attestation["timestamp"], "end": consent["expiry_timestamp"]},
            "message": "Attestation is valid under the given consent."
        }

    return {"valid": False, "message": "Attestation does not match consent conditions."}
