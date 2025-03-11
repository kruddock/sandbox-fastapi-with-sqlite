from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Album
    
router = APIRouter()


@router.get("/albums", response_model=list[Album])
async def list_albums(session: Session = Depends(get_session)) -> list:
    return session.exec(select(Album)).all()

@router.post("/albums", response_model=Album, status_code=201)
async def create_album(album: Album, session: Session = Depends(get_session)) -> Album:
    session.add(album)
    
    session.commit()
    
    session.refresh(album)
        
    return album

@router.get("/albums/{id}", response_model=Album)
async def show_album(id: int, session: Session = Depends(get_session)) -> Album:
    album = session.get(Album, id)
    
    if album is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return album

@router.put("/albums/{id}", response_model=Album)
async def update_album(id: int, album: Album, session: Session = Depends(get_session)) -> Album:
    target = session.get(Album, id)
    
    if target is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    for field, value in album.model_dump().items():
        setattr(target, field, value)
        
    session.commit()
    
    session.refresh(target)
    
    return target

@router.delete("/albums/{id}", status_code=204)
async def delete_album(id: int, session: Session = Depends(get_session)) -> None:
    album = session.get(Album, id)
    
    if album is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    session.delete(album)
    
    session.commit()
