from sqlmodel import Session, select
from typing import Annotated
from fastapi import Depends
from db import engine
from models import Team

class Repository:
    def __init__(self):
        with Session(engine) as session:
            self.session = session
        
    def listOf(self):
        return self.session.exec(select(Team)).all()
    
    def add(self, team: Team):
        self.session.add(team)
        
        self.session.commit()
        
        self.session.refresh(team)
        
        return team
   
def get_repo() -> Repository:
    return Repository() 
    
repos_dependency = Annotated[Repository, Depends(get_repo)]