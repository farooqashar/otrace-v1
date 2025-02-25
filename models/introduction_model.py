from pydantic import BaseModel

class Introduction(BaseModel):
    consumer: str  # The consumer (party being introduced)
    operator: str  # The operator (party making the introduction)
    service: str  # The service facilitating the introduction
