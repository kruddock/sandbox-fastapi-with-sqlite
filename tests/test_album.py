import pytest
import os
from typing import Final
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, delete
from dotenv import load_dotenv

from main import app
from repositories.repository_albums import AlbumRepository, get_repos
from models import Album

@pytest.fixture(name="engine")
def engine_fixture():
    load_dotenv()

    TEST_DATABASE_URI: Final[str] = os.getenv('TEST_DATABASE_URI', '')
    
    engine = create_engine(TEST_DATABASE_URI, connect_args={"check_same_thread": False})
    
    SQLModel.metadata.create_all(engine)
    
    yield engine

@pytest.fixture(name="client")  
def client_fixture(engine):
    def get_test_repos():
        return AlbumRepository(engine)  

    app.dependency_overrides[get_repos] = get_test_repos

    client = TestClient(app)  
    
    yield client
    
    app.dependency_overrides.clear()
    
    # load_dotenv()

    # TEST_DATABASE_URI: Final[str] = os.getenv('TEST_DATABASE_URI', '')
    
    # engine = create_engine(TEST_DATABASE_URI, connect_args={"check_same_thread": False})
    
    # SQLModel.metadata.create_all(engine)
    
    # def get_test_repos():
    #     return AlbumRepository(engine)  

    # app.dependency_overrides['repos'] = get_test_repos

    # client = TestClient(app)  
    
    # yield client
    
    # app.dependency_overrides.clear()

@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session

@pytest.fixture(name="cleanup")
def cleanup_fixture(engine):
    yield
    
    with Session(engine) as session:
        session.exec(delete(Album))
        session.commit()
        
def test_album_not_found(client: TestClient):
    response = client.get("/albums/999")  
    
    data = response.json()  

    assert response.status_code == 404
    assert data["detail"] == "Entity not found"

def test_create_an_album(client: TestClient):
    response = client.post(  
        "/albums/", json={ "title": "Blue Lights", "artist": "John Doe", "tracks": 10 }
    )
    
    data = response.json()  

    assert response.status_code == 201 
    assert data["title"] == "Blue Lights"  
    assert data["artist"] == "John Doe"  
    assert data["tracks"] == 10 
    assert data["id"] is not None 
        
def test_show_album(session: Session, client: TestClient):
    album = Album(title="D-E-F", artist="Michelle", tracks=11)
    session.add(album)
    session.commit()
    
    response = client.get(f"/albums/{album.id}")  
    
    data = response.json() 
    
    assert response.status_code == 200
    assert data["title"] == album.title
    assert data["artist"] == album.artist
    assert data["tracks"] == album.tracks
    assert data["id"] == album.id

def test_list_of_albums_is_empty(client: TestClient, cleanup: None):
    response = client.get( "/albums")

    data = response.json()  

    assert response.status_code == 200  
    assert len(data) == 2 
