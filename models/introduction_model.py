from pydantic import BaseModel

class Introduction(BaseModel):
    consumer: str  # The consumer (party making the introduction)
    operator: str  # The operator (party that will use the serive)
    service: str  # The service facilitating the tracing of data
