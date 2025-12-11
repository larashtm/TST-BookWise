"""
Unit tests for Loan entity
Target: 100% coverage for domain layer
"""
import pytest
from uuid import uuid4
from datetime import date, timedelta
from domain.loan import Loan
from domain.book_id import BookId
from domain.user_id import UserId
from domain.due_date import DueDate
from domain.loan_status import LoanStatus


class TestLoanCreation:
    """Test suite for Loan creation"""

    def test_create_loan_with_valid_data(self):
        """Test creating a loan with valid BookId and UserId"""
        book_id = BookId(uuid4())
        user_id = UserId(uuid4())
        
        loan = Loan(book_id, user_id)
        
        assert loan.loanId is not None
        assert loan.bookId == book_id
        assert loan.userId == user_id
        assert loan.loanStatus == LoanStatus.REQUESTED
        assert loan.dueDate is None
        assert loan.verified is False
        assert loan.approved is False

    def test_loan_has_unique_id(self):
        """Test that each loan has a unique ID"""
        book_id = BookId(uuid4())
        user_id = UserId(uuid4())
        
        loan1 = Loan(book_id, user_id)
        loan2 = Loan(book_id, user_id)
        
        assert loan1.loanId != loan2.loanId


class TestLoanVerification:
    """Test suite for loan verification"""

    def test_verify_requested_loan(self):
        """Test verifying a loan in REQUESTED status"""
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        
        loan.verify()
        
        assert loan.verified is True
        assert loan.loanStatus == LoanStatus.REQUESTED

    def test_verify_non_requested_loan_raises_error(self):
        """Test that verifying non-REQUESTED loan raises ValueError"""
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        due_date = DueDate(date.today() + timedelta(days=7))
        
        loan.verify()
        loan.approve(due_date)
        
        with pytest.raises(ValueError, match="not in requested state"):
            loan.verify()


class TestLoanApproval:
    """Test suite for loan approval"""

    def test_approve_verified_loan(self):
        """Test approving a verified loan"""
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        due_date = DueDate(date.today() + timedelta(days=7))
        
        loan.verify()
        loan.approve(due_date)
        
        assert loan.approved is True
        assert loan.loanStatus == LoanStatus.BORROWED
        assert loan.dueDate == due_date

    def test_approve_unverified_loan_raises_error(self):
        """Test that approving unverified loan raises ValueError"""
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        due_date = DueDate(date.today() + timedelta(days=7))
        
        with pytest.raises(ValueError, match="must be verified"):
            loan.approve(due_date)


class TestLoanReturn:
    """Test suite for loan return workflow"""

    def test_initiate_return_on_borrowed_loan(self):
        """Test initiating return on borrowed loan"""
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        due_date = DueDate(date.today() + timedelta(days=7))
        
        loan.borrow(due_date)
        loan.initiate_return()
        
        assert loan.return_initiated is True
        assert loan.loanStatus == LoanStatus.BORROWED

    def test_finalize_return_after_initiation(self):
        """Test finalizing return after initiation"""
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        due_date = DueDate(date.today() + timedelta(days=7))
        
        loan.borrow(due_date)
        loan.initiate_return()
        loan.finalize_return()
        
        assert loan.return_verified is True
        assert loan.loanStatus == LoanStatus.RETURNED
        assert loan.dueDate is None


class TestLoanExtension:
    """Test suite for loan extension"""

    def test_extend_loan_with_due_date(self):
        """Test extending loan with valid due date"""
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        original_date = date.today() + timedelta(days=7)
        due_date = DueDate(original_date)
        
        loan.borrow(due_date)
        new_due = loan.extend_loan(5)
        
        expected_date = original_date + timedelta(days=5)
        assert new_due.value == expected_date

    def test_extend_loan_without_due_date_raises_error(self):
        """Test that extending loan without due date raises ValueError"""
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        
        with pytest.raises(ValueError, match="No due date to extend"):
            loan.extend_loan(7)


class TestLoanWorkflow:
    """Test complete loan workflow"""

    def test_complete_loan_lifecycle(self):
        """Test complete loan workflow from creation to return"""
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        due_date = DueDate(date.today() + timedelta(days=7))
        
        # Request
        assert loan.loanStatus == LoanStatus.REQUESTED
        
        # Verify
        loan.verify()
        assert loan.verified is True
        
        # Approve
        loan.approve(due_date)
        assert loan.loanStatus == LoanStatus.BORROWED
        
        # Return
        loan.initiate_return()
        loan.finalize_return()
        assert loan.loanStatus == LoanStatus.RETURNED