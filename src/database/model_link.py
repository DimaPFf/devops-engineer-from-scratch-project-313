from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Link(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    original_url: str
    short_name: str
    short_url: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None