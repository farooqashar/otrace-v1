from fastapi import FastAPI
from routers import introduction, attestation, consent, data_use

app = FastAPI(title="OTrace V1")

# Include Routers
app.include_router(introduction.router)
app.include_router(attestation.router)
app.include_router(consent.router)
app.include_router(data_use.router)

@app.get("/")
def home():
    return {"message": "Welcome to OTrace V1 FastAPI Version!"}
