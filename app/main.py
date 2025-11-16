from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.contacts import router as contacts_router

app = FastAPI(title="Contacts API")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(contacts_router)


@app.get("/")
def root():
    return {"message": "Contacts API is running"}

