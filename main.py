from fastapi import FastAPI
from routers import introduction, attestation

app = FastAPI(title="OTrace V1")

# Include Routers
app.include_router(introduction.router)
app.include_router(attestation.router)

@app.get("/")
def home():
    return {"message": "Welcome to OTrace V1 FastAPI Version!"}
