from datetime import datetime
from typing import Optional

from sqlmodel import select

from src.database.connect_db import get_session
from src.database.model_link import Link
from src.utils.make_short_url import make_short_url
from src.services.utils.get_range import get_range


def get_all_links() -> list[Link]:
    with get_session() as session:
        return list(session.exec(select(Link)).all())

def get_links_with_pagination(range_pagination) -> list[Link]:
    with get_session() as session:
        range_data = get_range(range_pagination)
        if range_data is None:
            return []
        offset, limit = range_data
        return list(session.exec(select(Link).offset(offset).limit(limit)))


def create_link(original_url: str, short_name: str) -> Link:
    with get_session() as session:
        statement = select(Link).where(Link.short_name == short_name)
        find_link = session.exec(statement).one_or_none()
        if find_link:
            return find_link
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
