# app/main.py

from fastapi import FastAPI
from app.api.contacts import router as contacts_router

app = FastAPI(
    title="Contacts API",
    version="1.0.0"
)

# Підключаємо роутер контактів
app.include_router(contacts_router)


@app.get("/")
async def root():
    return {"message": "Contacts API is running"}
