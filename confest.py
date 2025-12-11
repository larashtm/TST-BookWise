import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from main import app
from domain.book_id import BookId
from domain.user_id import UserId
from domain.loan import Loan


@pytest.fixture
def test_client():
    """Fixture for FastAPI TestClient"""
    return TestClient(app)


@pytest.fixture
def sample_book_id():
    """Fixture for a sample BookId"""
    return BookId(uuid4())


@pytest.fixture
def sample_user_id():
    """Fixture for a sample UserId"""
    return UserId(uuid4())


@pytest.fixture
def sample_loan(sample_book_id, sample_user_id):
    """Fixture for a sample Loan"""
    return Loan(sample_book_id, sample_user_id)


@pytest.fixture
def peminjam_token(test_client):
    """Fixture to get authenticated peminjam token"""
    response = test_client.post(
        "/auth/login",
        data={"username": "peminjam1", "password": "pinjam123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def pengguna_token(test_client):
    """Fixture to get authenticated pengguna token"""
    response = test_client.post(
        "/auth/login",
        data={"username": "pengguna1", "password": "pengguna123"}
    )
    return response.json()["access_token"]