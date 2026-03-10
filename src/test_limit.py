from .main import app, limiter
from fastapi.testclient import TestClient
from fastapi import responses
from fastapi import status
import pytest

limitertest = limiter.enabled = False
client = TestClient(app=app)


def test_limited():
    response = client.get('/limited')
    assert response.status_code == status.HTTP_200_OK
