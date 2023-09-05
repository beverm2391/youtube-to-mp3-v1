from fastapi.testclient import TestClient
import pytest
from main import app  # Import your FastAPI instance here

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the YouTube to MP3 API. Use the /convert endpoint to get started."}

def test_invalid_url():
    response = client.get("/convert/", params={"url": "invalid_url"})
    assert response.status_code == 400  # Bad Request

def test_convert():
    # Replace with a short YouTube video URL for testing.
    youtube_url = "https://www.youtube.com/watch?v=__NeP0RqACU" # I'm using a video on YouTube's offician channe;
    response = client.get("/convert/", params={"url": youtube_url})
    
    # You can check for other response codes depending on the behavior of the test video URL.
    assert response.status_code == 200 or response.status_code == 404

    if response.status_code == 200:
        assert response.headers["content-type"] == "audio/mpeg"
