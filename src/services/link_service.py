from datetime import datetime
from typing import Optional

from sqlmodel import select

from src.database.connect_db import get_session
from src.database.model_link import Link
from src.utils.make_short_url import make_short_url


def get_all_links() -> list[Link]:
    with get_session() as session:
        return list(session.exec(select(Link)).all())


def create_link(original_url: str, short_name: str) -> Link:
    with get_session() as session:
        link = Link(
            original_url=original_url,
            short_name=short_name,
            short_url=make_short_url(short_name),
        )
        session.add(link)
        session.commit()
        session.refresh(link)
        return link


def get_link_by_id(link_id: int) -> Optional[Link]:
    with get_session() as session:
        return session.get(Link, link_id)


def delete_link(link_id: int) -> bool:
    with get_session() as session:
        link = session.get(Link, link_id)
        if link:
            session.delete(link)
            session.commit()
            return True
        return False


def update_link(
    link_id: int, original_url: str, short_name: str
) -> Optional[Link]:
    with get_session() as session:
        link = session.get(Link, link_id)
        if not link:
            return None
        link.original_url = original_url
        link.short_name = short_name
        link.short_url = make_short_url(short_name)
        link.updated_at = datetime.now()
        session.add(link)
        session.commit()
        session.refresh(link)
        return link
