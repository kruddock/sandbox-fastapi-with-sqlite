from fastapi import APIRouter
from repository import repos_dependency
from models import Team
    
router = APIRouter()


@router.get("/teams", response_model=list[Team])
async def list_teams(repos: repos_dependency) -> list:
    return repos.listOf()

@router.post("/teams", response_model=Team, status_code=201)
async def create_team(team: Team, repos: repos_dependency) -> Team:
    return repos.add(team)

# @router.get("/albums/{id}", response_model=Album)
# async def show_album(id: int, session: Session = Depends(get_session)) -> Album:
#     album = session.get(Album, id)
    
#     if album is None:
#         raise HTTPException(status_code=404, detail="Entity not found")
    
#     return album

# @router.put("/albums/{id}", response_model=Album)
# async def update_album(id: int, album: Album, session: Session = Depends(get_session)) -> Album:
#     target = session.get(Album, id)
    
#     if target is None:
#         raise HTTPException(status_code=404, detail="Entity not found")
    
#     for field, value in album.model_dump().items():
#         setattr(target, field, value)
        
#     session.commit()
    
#     session.refresh(target)
    
#     return target

# @router.delete("/albums/{id}", status_code=204)
# async def delete_album(id: int, session: Session = Depends(get_session)) -> None:
#     album = session.get(Album, id)
    
#     if album is None:
#         raise HTTPException(status_code=404, detail="Entity not found")
    
#     session.delete(album)
    
#     session.commit()
