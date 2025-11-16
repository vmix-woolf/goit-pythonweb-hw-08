import operator
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta
from sqlalchemy import select, or_
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


async def create_contact(session: AsyncSession, data: ContactCreate) -> Contact:
    new_contact = Contact(**data.model_dump())
    session.add(new_contact)
    await session.commit()
    await session.refresh(new_contact)
    return new_contact


async def get_contacts(session: AsyncSession) -> list[Contact]:
    result = await session.execute(select(Contact))
    return list(result.scalars().all())  # Приводимо до list — IDE замовкає


async def get_contact_by_id(session: AsyncSession, contact_id: int) -> Contact | None:
    stmt = select(Contact).where(operator.eq(Contact.id, contact_id))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_contact(
    session: AsyncSession,
    contact: Contact,
    data: ContactUpdate
) -> Contact:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)

    session.add(contact)
    await session.commit()
    await session.refresh(contact)
    return contact


async def delete_contact(session: AsyncSession, contact: Contact) -> None:
    await session.delete(contact)
    await session.commit()



async def search_contacts(
    session: AsyncSession,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
):
    filters = []

    if first_name:
        filters.append(Contact.first_name.ilike(f"%{first_name}%"))

    if last_name:
        filters.append(Contact.last_name.ilike(f"%{last_name}%"))

    if email:
        filters.append(Contact.email.ilike(f"%{email}%"))

    if not filters:
        # Немає параметрів → повернути порожній список
        return []

    stmt = select(Contact).where(or_(*filters))
    result = await session.execute(stmt)
    return result.scalars().all()



async def get_upcoming_birthdays(session: AsyncSession):
    today = date.today()
    target = today + timedelta(days=7)

    stmt = select(Contact)
    result = await session.execute(stmt)
    contacts = result.scalars().all()

    upcoming = []

    for c in contacts:
        if not c.birthday:
            continue

        # Наводимо ДР до цього року
        bd_this_year = c.birthday.replace(year=today.year)
        if today <= bd_this_year <= target:
            upcoming.append(c)

    return upcoming
