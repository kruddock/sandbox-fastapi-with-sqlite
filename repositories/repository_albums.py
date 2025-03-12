import contextlib
from typing import Annotated
from sqlmodel import Session, select
from fastapi import Depends
from repositories.database import engine
from repositories.base import BaseRespository
from models import Album

class AlbumRepository(BaseRespository[Album]):
    @contextlib.contextmanager
    def get_session(self):
        with Session(engine) as session:
            yield session
            
    def collection(self):
        with self.get_session() as session:
            return session.exec(select(Album)).all()
        
    def add(self, album: Album):
        with self.get_session() as session:
            session.add(album)
            
            session.commit()
            
            session.refresh(album)
            
            return album
        
    def show(self, id: int) -> Album | None:
        with self.get_session() as session:
            album = session.get(Album, id)
            
            return album

    def update(self, id: int, album: Album) -> Album | None:
        with self.get_session() as session:
            target = session.get(Album, id)

            if target is not None:
                for field, value in album.model_dump().items():
                    setattr(target, field, value)
        
                session.commit()
    
                session.refresh(target)
            
            return target
        
    
    def remove(self, id: int) -> None:
        with self.get_session() as session:
            album = session.get(Album, id)
            
            if album is not None:
                session.delete(album)
    
                session.commit()
                
            return album
        
def get_repos() -> AlbumRepository:
    return AlbumRepository() 

Repos = Annotated[AlbumRepository, Depends(get_repos)]