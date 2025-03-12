from fastapi import APIRouter, HTTPException
from repositories.repository_albums import Repos
from models import Album
    
router = APIRouter()

@router.get("/albums", response_model=list[Album])
async def list_of_albums(repos: Repos) -> list:
    return repos.collection()

@router.post("/albums", response_model=Album, status_code=201)
async def create_an_album(album: Album, repos: Repos) -> Album:
    return repos.add(album)

@router.get("/albums/{id}", response_model=Album)
async def find_album_by_id(id: int, repos: Repos) -> Album:
    album = repos.show(id)
    
    if album is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return album

@router.put("/albums/{id}", response_model=Album)
async def update_album(id: int, album: Album, repos: Repos) -> Album:
    modified = repos.update(id, album)
    
    if modified is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return modified

@router.delete("/albums/{id}", status_code=204)
async def delete_album(id: int, repos: Repos) -> None:
    deleted = repos.remove(id)
    
    if deleted is None:
        raise HTTPException(status_code=404, detail="Entity not found")
