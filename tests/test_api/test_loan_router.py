import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from main import app
from infrastructure.in_memory_loan_repository import InMemoryLoanRepository
from api.loan_router import repo


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_repo():
    """Reset repository before each test"""
    repo.data.clear()
    yield
    repo.data.clear()


@pytest.fixture
def peminjam_token():
    """Fixture to get peminjam auth token"""
    response = client.post(
        "/auth/login",
        data={"username": "peminjam1", "password": "pinjam123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def pengguna_token():
    """Fixture to get pengguna auth token"""
    response = client.post(
        "/auth/login",
        data={"username": "pengguna1", "password": "pengguna123"}
    )
    return response.json()["access_token"]


class TestCreateLoan:
    """Test suite for POST /loans"""

    def test_create_loan_success(self, peminjam_token):
        """Test creating a loan successfully"""
        response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(uuid4())
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "loanId" in data
        assert data["status"] == "requested"
        assert data["verified"] is False
        assert data["approved"] is False

    def test_create_loan_without_auth(self):
        """Test creating loan without authentication fails"""
        response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(uuid4())
            }
        )
        
        assert response.status_code == 401

    def test_create_loan_with_pengguna_role_fails(self, pengguna_token):
        """Test creating loan with pengguna role fails"""
        response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(uuid4())
            },
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        
        assert response.status_code == 403

    def test_create_loan_invalid_uuid(self, peminjam_token):
        """Test creating loan with invalid UUID"""
        response = client.post(
            "/loans",
            json={
                "bookId": "invalid-uuid",
                "userId": str(uuid4())
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        assert response.status_code == 422

    def test_create_loan_missing_fields(self, peminjam_token):
        """Test creating loan with missing fields"""
        response = client.post(
            "/loans",
            json={"bookId": str(uuid4())},
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        assert response.status_code == 422


class TestListMyLoans:
    """Test suite for GET /loans/my"""

    def test_list_my_loans_empty(self, peminjam_token):
        """Test listing loans when user has none"""
        response = client.get(
            "/loans/my",
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        assert response.status_code == 200
        assert response.json() == []

    def test_list_my_loans_with_loans(self, peminjam_token):
        """Test listing loans when user has loans"""
        # Create a loan first
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        
        client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(user.user_id)
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        response = client.get(
            "/loans/my",
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_list_my_loans_without_auth(self):
        """Test listing loans without authentication"""
        response = client.get("/loans/my")
        
        assert response.status_code == 401

    def test_list_my_loans_with_pengguna_fails(self, pengguna_token):
        """Test listing my loans with pengguna role fails"""
        response = client.get(
            "/loans/my",
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        
        assert response.status_code == 403


class TestListAllLoans:
    """Test suite for GET /loans/all"""

    def test_list_all_loans_empty(self, pengguna_token):
        """Test listing all loans when none exist"""
        response = client.get(
            "/loans/all",
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        
        assert response.status_code == 200
        assert response.json() == []

    def test_list_all_loans_with_data(self, pengguna_token, peminjam_token):
        """Test listing all loans when loans exist"""
        # Create a loan
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        
        client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(user.user_id)
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        response = client.get(
            "/loans/all",
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_list_all_loans_without_auth(self):
        """Test listing all loans without authentication"""
        response = client.get("/loans/all")
        
        assert response.status_code == 401

    def test_list_all_loans_with_peminjam_fails(self, peminjam_token):
        """Test listing all loans with peminjam role fails"""
        response = client.get(
            "/loans/all",
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        assert response.status_code == 403


class TestGetLoanById:
    """Test suite for GET /loans/{loan_id}"""

    def test_get_loan_by_id_success(self, peminjam_token):
        """Test getting loan by ID successfully"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        
        # Create loan
        create_response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(user.user_id)
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        loan_id = create_response.json()["loanId"]
        
        # Get loan
        response = client.get(
            f"/loans/{loan_id}",
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["loanId"] == loan_id

    def test_get_loan_not_found(self, peminjam_token):
        """Test getting non-existent loan"""
        fake_id = str(uuid4())
        
        response = client.get(
            f"/loans/{fake_id}",
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        assert response.status_code == 404

    def test_get_loan_forbidden_different_user(self, peminjam_token):
        """Test getting another user's loan as peminjam"""
        # Create loan with different user
        other_user_id = str(uuid4())
        
        create_response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": other_user_id
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        loan_id = create_response.json()["loanId"]
        
        # Try to get it (will fail because userId doesn't match token)
        response = client.get(
            f"/loans/{loan_id}",
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        assert response.status_code == 403

    def test_get_loan_as_pengguna_success(self, pengguna_token, peminjam_token):
        """Test pengguna can get any loan"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        
        # Create loan as peminjam
        create_response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(user.user_id)
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        loan_id = create_response.json()["loanId"]
        
        # Get as pengguna
        response = client.get(
            f"/loans/{loan_id}",
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        
        assert response.status_code == 200


class TestVerifyLoan:
    """Test suite for POST /loans/{loan_id}/verify"""

    def test_verify_loan_success(self, pengguna_token, peminjam_token):
        """Test verifying a loan successfully"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        
        # Create loan
        create_response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(user.user_id)
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        loan_id = create_response.json()["loanId"]
        
        # Verify loan
        response = client.post(
            f"/loans/{loan_id}/verify",
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        
        assert response.status_code == 200
        assert "verified" in response.json()["detail"].lower()

    def test_verify_loan_not_found(self, pengguna_token):
        """Test verifying non-existent loan"""
        fake_id = str(uuid4())
        
        response = client.post(
            f"/loans/{fake_id}/verify",
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        
        assert response.status_code == 404

    def test_verify_loan_as_peminjam_fails(self, peminjam_token):
        """Test that peminjam cannot verify loans"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        
        create_response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(user.user_id)
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        loan_id = create_response.json()["loanId"]
        
        response = client.post(
            f"/loans/{loan_id}/verify",
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        assert response.status_code == 403


class TestApproveLoan:
    """Test suite for POST /loans/{loan_id}/approve"""

    def test_approve_loan_success(self, pengguna_token, peminjam_token):
        """Test approving a loan successfully"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        
        # Create and verify loan
        create_response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(user.user_id)
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        loan_id = create_response.json()["loanId"]
        
        client.post(
            f"/loans/{loan_id}/verify",
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        
        # Approve loan
        response = client.post(
            f"/loans/{loan_id}/approve",
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        
        assert response.status_code == 200
        assert "approved" in response.json()["detail"].lower()
        assert "dueDate" in response.json()

    def test_approve_unverified_loan_fails(self, pengguna_token, peminjam_token):
        """Test approving unverified loan fails"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        
        create_response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(user.user_id)
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        loan_id = create_response.json()["loanId"]
        
        response = client.post(
            f"/loans/{loan_id}/approve",
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        
        assert response.status_code == 400


class TestInitiateReturn:
    """Test suite for POST /loans/{loan_id}/return"""

    def test_initiate_return_success(self, peminjam_token, pengguna_token):
        """Test initiating return successfully"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        
        # Create, verify, and approve loan
        create_response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(user.user_id)
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        loan_id = create_response.json()["loanId"]
        
        client.post(
            f"/loans/{loan_id}/verify",
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        client.post(
            f"/loans/{loan_id}/approve",
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        
        # Initiate return
        response = client.post(
            f"/loans/{loan_id}/return",
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        assert response.status_code == 200
        assert "initiated" in response.json()["detail"].lower()


class TestFinalizeReturn:
    """Test suite for POST /loans/{loan_id}/finalize-return"""

    def test_finalize_return_success(self, peminjam_token, pengguna_token):
        """Test finalizing return successfully"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        
        # Full workflow
        create_response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(user.user_id)
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        loan_id = create_response.json()["loanId"]
        
        client.post(f"/loans/{loan_id}/verify", headers={"Authorization": f"Bearer {pengguna_token}"})
        client.post(f"/loans/{loan_id}/approve", headers={"Authorization": f"Bearer {pengguna_token}"})
        client.post(f"/loans/{loan_id}/return", headers={"Authorization": f"Bearer {peminjam_token}"})
        
        # Finalize return
        response = client.post(
            f"/loans/{loan_id}/finalize-return",
            headers={"Authorization": f"Bearer {pengguna_token}"}
        )
        
        assert response.status_code == 200


class TestExtendLoan:
    """Test suite for POST /loans/{loan_id}/extend"""

    def test_extend_loan_success(self, peminjam_token, pengguna_token):
        """Test extending loan successfully"""
        from auth.users import get_user_by_username
        user = get_user_by_username("peminjam1")
        
        # Create and approve loan
        create_response = client.post(
            "/loans",
            json={
                "bookId": str(uuid4()),
                "userId": str(user.user_id)
            },
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        loan_id = create_response.json()["loanId"]
        
        client.post(f"/loans/{loan_id}/verify", headers={"Authorization": f"Bearer {pengguna_token}"})
        client.post(f"/loans/{loan_id}/approve", headers={"Authorization": f"Bearer {pengguna_token}"})
        
        # Extend loan
        response = client.post(
            f"/loans/{loan_id}/extend",
            json={"extra_days": 5},
            headers={"Authorization": f"Bearer {peminjam_token}"}
        )
        
        assert response.status_code == 200
        assert "newDueDate" in response.json()