from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.contact import get_upcoming_birthdays as crud_birthdays
from app.database import get_session
from app.crud.contact import (
    create_contact,
    get_contact_by_id,
    get_contacts,
    update_contact,
    delete_contact,
    search_contacts,
)
from app.schemas.contact import ContactCreate, ContactUpdate, ContactOut

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", response_model=ContactOut)
async def create_contact_api(
    data: ContactCreate, session: AsyncSession = Depends(get_session)
):
    return await create_contact(session, data)


@router.get("/", response_model=list[ContactOut])
async def list_contacts_api(session: AsyncSession = Depends(get_session)):
    return await get_contacts(session)


@router.get("/{contact_id}", response_model=ContactOut)
async def get_contact_api(contact_id: int, session: AsyncSession = Depends(get_session)):
    contact = await get_contact_by_id(session, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactOut)
async def update_contact_api(
    contact_id: int, data: ContactUpdate, session: AsyncSession = Depends(get_session)
):
    contact = await get_contact_by_id(session, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return await update_contact(session, contact, data)

@router.get("/search", response_model=list[ContactOut])
async def search_contacts_endpoint(
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    return await search_contacts(
        session=session,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )


@router.get("/birthdays", response_model=list[ContactOut])
async def birthdays_endpoint(
    session: AsyncSession = Depends(get_session),
):
    return await crud_birthdays(session)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact_api(contact_id: int, session: AsyncSession = Depends(get_session)):
    contact = await get_contact_by_id(session, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    await delete_contact(session, contact)
    return None
