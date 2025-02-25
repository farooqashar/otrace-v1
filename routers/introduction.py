from fastapi import APIRouter, HTTPException
from models.introduction_model import Introduction

router = APIRouter(prefix="/introduction", tags=["Introduction"])

introductions = []

@router.post("/introduce/")
def introduce(intro: Introduction):
    introductions.append(intro)

    return {
        "message": f"{intro.consumer} has been introduced to {intro.operator} via {intro.service}",
        "introduction": intro
    }

@router.get("/introduced/{consumer}/{operator}")
def introduced(consumer: str, operator: str):
    """
    Checks if an operator is connected to any service on behalf of a consumer.
    """
    for intro in introductions:
        if intro.consumer == consumer and intro.operator == operator:
            return {"consumer": consumer, "operator": operator, "service": intro.service}

    raise HTTPException(status_code=404, detail="No introduction found")
