from typing import Annotated
from sqlmodel import select
from fastapi import Depends
from repositories.database import engine
from repositories.base import BaseRespository
from models import Team

class TeamRepository(BaseRespository[Team]):
    def collection(self):
        with self.get_session() as session:
            return session.exec(select(Team)).all()
        
    def add(self, team: Team):
        with self.get_session() as session:
            session.add(team)
            
            session.commit()
            
            session.refresh(team)
            
            return team
        
    def show(self, id: int) -> Team | None:
        with self.get_session() as session:
            team = session.get(Team, id)
            
            return team

    def update(self, id: int, team: Team) -> Team | None:
        with self.get_session() as session:
            target = session.get(Team, id)

            if target is not None:
                for field, value in team.model_dump().items():
                    setattr(target, field, value)
        
                session.commit()
    
                session.refresh(target)
            
            return target
        
    
    def remove(self, id: int) -> None:
        with self.get_session() as session:
            team = session.get(Team, id)
            
            if team is not None:
                session.delete(team)
    
                session.commit()
                
            return team
        
def get_repos() -> TeamRepository:
    return TeamRepository(engine) 

Repos = Annotated[TeamRepository, Depends(get_repos)]

