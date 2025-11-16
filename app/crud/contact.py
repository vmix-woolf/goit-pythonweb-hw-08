import operator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
