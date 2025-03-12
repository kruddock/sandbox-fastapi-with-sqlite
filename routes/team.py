from fastapi import APIRouter, HTTPException
from repositories.repository_teams import Repos
from models import Team
    
router = APIRouter()


@router.get("/teams", response_model=list[Team])
async def list_of_teams(repos: Repos) -> list:
    return repos.collection()

@router.post("/teams", response_model=Team, status_code=201)
async def create_team(team: Team, repos: Repos) -> Team:
    return repos.add(team)

@router.get("/teams/{id}", response_model=Team)
async def find_team_by_id(id: int, repos: Repos) -> Team:
    team = repos.show(id)
    
    if team is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return team

@router.put("/teams/{id}", response_model=Team)
async def update_team(id: int, team: Team, repos: Repos) -> Team:
    modified = repos.update(id, team)
    
    if modified is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return modified

@router.delete("/teams/{id}", status_code=204)
async def delete_team(id: int, repos: Repos) -> None:
    deleted = repos.remove(id)
    
    if deleted is None:
        raise HTTPException(status_code=404, detail="Entity not found")
