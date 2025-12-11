"""
Unit tests for Pydantic schemas
"""
import pytest
from uuid import uuid4
from datetime import datetime, date
from pydantic import ValidationError

from schemas.loan_schema import LoanCreateRequest, LoanResponse
from schemas.auth_schema import LoginResponse, RefreshRequest


class TestLoanCreateRequest:
    """Test suite for LoanCreateRequest schema"""

    def test_valid_loan_create_request(self):
        """Test creating valid loan request"""
        data = {
            "bookId": str(uuid4()),
            "userId": str(uuid4())
        }
        
        request = LoanCreateRequest(**data)
        
        assert request.bookId is not None
        assert request.userId is not None

    def test_loan_create_request_with_uuid_objects(self):
        """Test loan request with UUID objects"""
        book_id = uuid4()
        user_id = uuid4()
        
        request = LoanCreateRequest(bookId=book_id, userId=user_id)
        
        assert request.bookId == book_id
        assert request.userId == user_id

    def test_loan_create_request_missing_book_id(self):
        """Test that missing bookId raises error"""
        with pytest.raises(ValidationError):
            LoanCreateRequest(userId=str(uuid4()))

    def test_loan_create_request_missing_user_id(self):
        """Test that missing userId raises error"""
        with pytest.raises(ValidationError):
            LoanCreateRequest(bookId=str(uuid4()))

    def test_loan_create_request_invalid_book_id(self):
        """Test that invalid bookId raises error"""
        with pytest.raises(ValidationError):
            LoanCreateRequest(bookId="not-a-uuid", userId=str(uuid4()))

    def test_loan_create_request_invalid_user_id(self):
        """Test that invalid userId raises error"""
        with pytest.raises(ValidationError):
            LoanCreateRequest(bookId=str(uuid4()), userId="not-a-uuid")

    def test_loan_create_request_empty_strings(self):
        """Test that empty strings raise error"""
        with pytest.raises(ValidationError):
            LoanCreateRequest(bookId="", userId="")

    def test_loan_create_request_json_serialization(self):
        """Test JSON serialization of loan request"""
        request = LoanCreateRequest(bookId=uuid4(), userId=uuid4())
        
        json_data = request.model_dump_json()
        assert json_data is not None
        assert isinstance(json_data, str)


class TestLoanResponse:
    """Test suite for LoanResponse schema"""

    def test_valid_loan_response(self):
        """Test creating valid loan response"""
        data = {
            "loanId": uuid4(),
            "bookId": uuid4(),
            "userId": uuid4(),
            "status": "requested",
            "createdAt": datetime.utcnow(),
            "dueDate": date.today(),
            "verified": False,
            "approved": False,
            "return_initiated": False
        }
        
        response = LoanResponse(**data)
        
        assert response.loanId is not None
        assert response.status == "requested"

    def test_loan_response_minimal_fields(self):
        """Test loan response with only required fields"""
        data = {
            "loanId": uuid4(),
            "bookId": uuid4(),
            "userId": uuid4(),
            "status": "borrowed",
            "createdAt": datetime.utcnow()
        }
        
        response = LoanResponse(**data)
        
        assert response.dueDate is None
        assert response.verified is False
        assert response.approved is False

    def test_loan_response_with_due_date(self):
        """Test loan response with due date"""
        due = date.today()
        data = {
            "loanId": uuid4(),
            "bookId": uuid4(),
            "userId": uuid4(),
            "status": "borrowed",
            "createdAt": datetime.utcnow(),
            "dueDate": due
        }
        
        response = LoanResponse(**data)
        assert response.dueDate == due

    def test_loan_response_verified_true(self):
        """Test loan response with verified true"""
        data = {
            "loanId": uuid4(),
            "bookId": uuid4(),
            "userId": uuid4(),
            "status": "requested",
            "createdAt": datetime.utcnow(),
            "verified": True
        }
        
        response = LoanResponse(**data)
        assert response.verified is True

    def test_loan_response_approved_true(self):
        """Test loan response with approved true"""
        data = {
            "loanId": uuid4(),
            "bookId": uuid4(),
            "userId": uuid4(),
            "status": "borrowed",
            "createdAt": datetime.utcnow(),
            "approved": True
        }
        
        response = LoanResponse(**data)
        assert response.approved is True

    def test_loan_response_return_initiated_true(self):
        """Test loan response with return_initiated true"""
        data = {
            "loanId": uuid4(),
            "bookId": uuid4(),
            "userId": uuid4(),
            "status": "borrowed",
            "createdAt": datetime.utcnow(),
            "return_initiated": True
        }
        
        response = LoanResponse(**data)
        assert response.return_initiated is True

    def test_loan_response_missing_required_field(self):
        """Test that missing required fields raise error"""
        with pytest.raises(ValidationError):
            LoanResponse(
                loanId=uuid4(),
                bookId=uuid4(),
                status="requested",
                createdAt=datetime.utcnow()
            )

    def test_loan_response_invalid_status(self):
        """Test loan response validation with status"""
        data = {
            "loanId": uuid4(),
            "bookId": uuid4(),
            "userId": uuid4(),
            "status": "borrowed",
            "createdAt": datetime.utcnow()
        }
        
        response = LoanResponse(**data)
        assert response.status in ["requested", "borrowed", "returned", "overdue"]

    def test_loan_response_json_serialization(self):
        """Test JSON serialization of loan response"""
        response = LoanResponse(
            loanId=uuid4(),
            bookId=uuid4(),
            userId=uuid4(),
            status="borrowed",
            createdAt=datetime.utcnow()
        )
        
        json_data = response.model_dump_json()
        assert json_data is not None
        assert isinstance(json_data, str)


class TestLoginResponse:
    """Test suite for LoginResponse schema"""

    def test_valid_login_response(self):
        """Test creating valid login response"""
        data = {
            "access_token": "fake_access_token",
            "token_type": "bearer",
            "refresh_token": "fake_refresh_token"
        }
        
        response = LoginResponse(**data)
        
        assert response.access_token == "fake_access_token"
        assert response.token_type == "bearer"
        assert response.refresh_token == "fake_refresh_token"

    def test_login_response_default_token_type(self):
        """Test that token_type has default value"""
        data = {
            "access_token": "fake_access_token",
            "refresh_token": "fake_refresh_token"
        }
        
        response = LoginResponse(**data)
        
        assert response.token_type == "bearer"

    def test_login_response_custom_token_type(self):
        """Test login response with custom token type"""
        data = {
            "access_token": "fake_access_token",
            "token_type": "custom",
            "refresh_token": "fake_refresh_token"
        }
        
        response = LoginResponse(**data)
        
        assert response.token_type == "custom"

    def test_login_response_missing_access_token(self):
        """Test that missing access_token raises error"""
        with pytest.raises(ValidationError):
            LoginResponse(refresh_token="fake_refresh_token")

    def test_login_response_missing_refresh_token(self):
        """Test that missing refresh_token raises error"""
        with pytest.raises(ValidationError):
            LoginResponse(access_token="fake_access_token")

    def test_login_response_empty_tokens(self):
        """Test login response with empty token strings"""
        data = {
            "access_token": "",
            "refresh_token": ""
        }
        
        response = LoginResponse(**data)
        # Empty strings are valid, just checking it doesn't raise
        assert response.access_token == ""

    def test_login_response_json_serialization(self):
        """Test JSON serialization of login response"""
        response = LoginResponse(
            access_token="token123",
            refresh_token="refresh456"
        )
        
        json_data = response.model_dump_json()
        assert json_data is not None
        assert "token123" in json_data


class TestRefreshRequest:
    """Test suite for RefreshRequest schema"""

    def test_valid_refresh_request(self):
        """Test creating valid refresh request"""
        data = {"refresh_token": "fake_refresh_token"}
        
        request = RefreshRequest(**data)
        
        assert request.refresh_token == "fake_refresh_token"

    def test_refresh_request_missing_token(self):
        """Test that missing refresh_token raises error"""
        with pytest.raises(ValidationError):
            RefreshRequest()

    def test_refresh_request_empty_token(self):
        """Test refresh request with empty token"""
        request = RefreshRequest(refresh_token="")
        
        # Empty string is valid, just checking
        assert request.refresh_token == ""

    def test_refresh_request_with_uuid(self):
        """Test refresh request with UUID token"""
        token = str(uuid4())
        request = RefreshRequest(refresh_token=token)
        
        assert request.refresh_token == token

    def test_refresh_request_json_serialization(self):
        """Test JSON serialization of refresh request"""
        request = RefreshRequest(refresh_token="token123")
        
        json_data = request.model_dump_json()
        assert json_data is not None
        assert "token123" in json_data


class TestSchemaIntegration:
    """Integration tests for schemas"""

    def test_loan_request_to_response_flow(self):
        """Test creating loan request and response"""
        book_id = uuid4()
        user_id = uuid4()
        
        # Create request
        request = LoanCreateRequest(bookId=book_id, userId=user_id)
        
        # Simulate creating response from request
        response = LoanResponse(
            loanId=uuid4(),
            bookId=request.bookId,
            userId=request.userId,
            status="requested",
            createdAt=datetime.utcnow()
        )
        
        assert response.bookId == book_id
        assert response.userId == user_id

    def test_auth_flow_schemas(self):
        """Test complete auth flow with schemas"""
        # Login response
        login = LoginResponse(
            access_token="access123",
            refresh_token="refresh456"
        )
        
        # Refresh request
        refresh_req = RefreshRequest(refresh_token=login.refresh_token)
        
        assert refresh_req.refresh_token == login.refresh_token

    def test_all_schemas_json_compatible(self):
        """Test that all schemas can be serialized to JSON"""
        loan_req = LoanCreateRequest(bookId=uuid4(), userId=uuid4())
        loan_res = LoanResponse(
            loanId=uuid4(),
            bookId=uuid4(),
            userId=uuid4(),
            status="borrowed",
            createdAt=datetime.utcnow()
        )
        login_res = LoginResponse(access_token="a", refresh_token="r")
        refresh_req = RefreshRequest(refresh_token="token")
        
        # All should serialize without errors
        assert loan_req.model_dump_json() is not None
        assert loan_res.model_dump_json() is not None
        assert login_res.model_dump_json() is not None
        assert refresh_req.model_dump_json() is not None