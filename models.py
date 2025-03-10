from typing import Optional

from sqlmodel import Field, SQLModel

class Album(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    artist: str
    tracks: int
    is_local: bool = False