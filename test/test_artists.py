from fastapi.testclient import TestClient
from App.main import app
from App.database import get_db
from App.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal() 
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_artist():
    response = client.post(
        "/artists/",
        json={"name": "Test Artist", "genre": "Test Genre", "country": "Test Country"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Artist"
    assert "id" in data

def test_read_artist():
    response = client.get("/artists/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Artist"

def test_read_artists():
    response = client.get("/artists/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_update_artist():
    response = client.put(
        "/artists/1",
        json={"name": "Updated Artist", "genre": "Updated Genre", "country": "Updated Country"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Artist"

def test_delete_artist():
    response = client.delete("/artists/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Artist"

    response = client.get("/artists/1")
    assert response.status_code == 404