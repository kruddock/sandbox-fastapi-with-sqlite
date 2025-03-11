import os
from typing import Final
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
from models import Album, Team

load_dotenv()

DATABASE_URI: Final[str] = os.getenv('DATABASE_URI', '')

engine = create_engine(DATABASE_URI, echo=True)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    
def seed() -> None:
    album1 = Album(title="A-B-C", artist="John Doe", tracks=20)
    album2 = Album(title="1-2-3", artist="Jane Doe", tracks=8)
    album3 = Album(title="Essence", artist="Justin", tracks=12)
    album4 = Album(title="My Life", artist="Alexis", tracks=12, is_local=True)
    
    team1 = Team(name="Laker",championships=17,last_championship=2020)
    team2 = Team(name="Celtics",championships=18,last_championship=2024)
    team3 = Team(name="Heat",championships=3,last_championship=2013)
    team4 = Team(name="Cavaliers",championships=1,last_championship=2017)

    with Session(engine) as session:
        session.add_all([album1, album2, album3, album4, team1, team2, team3, team4])
        session.commit()
    
def get_session():
    with Session(engine) as session:
        yield session
        
