import os
from typing import Final
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
from models import Album

load_dotenv()

DATABASE_URI: Final[str] = os.getenv('DATABASE_URI', '')

engine = create_engine(DATABASE_URI, echo=True)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    
def seed() -> None:
    album1 = Album(title="Winterfall", artist="Dave Wilson", tracks=20)
    album2 = Album(title="1-2-3", artist="Pedro Parqueador", tracks=8)
    album3 = Album(title="Essence", artist="Jean Jones", tracks=12)
    album4 = Album(title="Angella", artist="Angella", tracks=12, is_local=True)

    with Session(engine) as session:
        session.add_all([album1, album2, album3, album4])
        session.commit()
    
def get_session():
    with Session(engine) as session:
        yield session
        
