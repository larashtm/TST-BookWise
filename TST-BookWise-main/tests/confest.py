"""
Pytest configuration and shared fixtures
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from main import app
from domain.book_id import BookId
from domain.user_id import UserId
from domain.loan import Loan
from infrastructure.in_memory_loan_repository import InMemoryLoanRepository


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
def empty_repository():
    """Fixture for an empty repository"""
    return InMemoryLoanRepository()


@pytest.fixture
def populated_repository(sample_loan):
    """Fixture for a repository with sample data"""
    repo = InMemoryLoanRepository()
    repo.save(sample_loan)
    return repo


@pytest.fixture(autouse=False)
def reset_repository():
    """Fixture to reset repository between tests"""
    from api.loan_router import repo
    original_data = repo.data.copy()
    yield
    repo.data = original_data


@pytest.fixture
def peminjam_credentials():
    """Fixture for peminjam credentials"""
    return {"username": "peminjam1", "password": "pinjam123"}


@pytest.fixture
def pengguna_credentials():
    """Fixture for pengguna credentials"""
    return {"username": "pengguna1", "password": "pengguna123"}


@pytest.fixture
def peminjam_token(test_client, peminjam_credentials):
    """Fixture to get authenticated peminjam token"""
    response = test_client.post(
        "/auth/login",
        data=peminjam_credentials
    )
    return response.json()["access_token"]


@pytest.fixture
def pengguna_token(test_client, pengguna_credentials):
    """Fixture to get authenticated pengguna token"""
    response = test_client.post(
        "/auth/login",
        data=pengguna_credentials
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers_peminjam(peminjam_token):
    """Fixture for peminjam authorization headers"""
    return {"Authorization": f"Bearer {peminjam_token}"}


@pytest.fixture
def auth_headers_pengguna(pengguna_token):
    """Fixture for pengguna authorization headers"""
    return {"Authorization": f"Bearer {pengguna_token}"}