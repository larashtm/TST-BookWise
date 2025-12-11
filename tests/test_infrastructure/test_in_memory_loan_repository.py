import pytest
from uuid import uuid4
from domain.loan import Loan
from domain.book_id import BookId
from domain.user_id import UserId
from infrastructure.in_memory_loan_repository import InMemoryLoanRepository


class TestRepositoryInitialization:
    """Test suite for repository initialization"""

    def test_repository_initialization(self):
        """Test repository initializes with empty data"""
        repo = InMemoryLoanRepository()
        assert repo.data == {}
        assert isinstance(repo.data, dict)

    def test_repository_initial_state(self):
        """Test repository starts empty"""
        repo = InMemoryLoanRepository()
        assert len(repo.data) == 0
        assert repo.list_all() == []


class TestRepositorySave:
    """Test suite for save operations"""

    def test_save_new_loan(self):
        """Test saving a new loan"""
        repo = InMemoryLoanRepository()
        book_id = BookId(uuid4())
        user_id = UserId(uuid4())
        loan = Loan(book_id, user_id)
        
        repo.save(loan)
        
        assert str(loan.loanId) in repo.data
        assert repo.data[str(loan.loanId)] == loan

    def test_save_updates_existing_loan(self):
        """Test saving updates existing loan"""
        repo = InMemoryLoanRepository()
        book_id = BookId(uuid4())
        user_id = UserId(uuid4())
        loan = Loan(book_id, user_id)
        
        repo.save(loan)
        loan.verify()
        repo.save(loan)
        
        retrieved = repo.findById(loan.loanId)
        assert retrieved.verified is True

    def test_save_multiple_loans(self):
        """Test saving multiple loans"""
        repo = InMemoryLoanRepository()
        loans = [Loan(BookId(uuid4()), UserId(uuid4())) for _ in range(3)]
        
        for loan in loans:
            repo.save(loan)
        
        assert len(repo.data) == 3

    def test_overwrite_loan_same_id(self):
        """Test that saving loan with same ID overwrites"""
        repo = InMemoryLoanRepository()
        book_id = BookId(uuid4())
        user_id = UserId(uuid4())
        loan = Loan(book_id, user_id)
        
        repo.save(loan)
        initial_verified = loan.verified
        
        loan.verify()
        repo.save(loan)
        
        retrieved = repo.findById(loan.loanId)
        assert retrieved.verified != initial_verified
        assert len(repo.list_all()) == 1


class TestRepositoryFindById:
    """Test suite for findById operations"""

    def test_find_by_id_existing_loan(self):
        """Test finding loan by ID that exists"""
        repo = InMemoryLoanRepository()
        book_id = BookId(uuid4())
        user_id = UserId(uuid4())
        loan = Loan(book_id, user_id)
        
        repo.save(loan)
        found = repo.findById(loan.loanId)
        
        assert found == loan
        assert found.loanId == loan.loanId

    def test_find_by_id_non_existing_loan(self):
        """Test finding loan by ID that doesn't exist"""
        repo = InMemoryLoanRepository()
        non_existing_id = uuid4()
        
        found = repo.findById(non_existing_id)
        
        assert found is None

    def test_find_by_id_with_string_id(self):
        """Test finding loan by string ID"""
        repo = InMemoryLoanRepository()
        book_id = BookId(uuid4())
        user_id = UserId(uuid4())
        loan = Loan(book_id, user_id)
        
        repo.save(loan)
        found = repo.findById(str(loan.loanId))
        
        assert found == loan

    def test_find_by_id_returns_exact_loan(self):
        """Test that findById returns the exact loan object"""
        repo = InMemoryLoanRepository()
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        
        repo.save(loan)
        found = repo.findById(loan.loanId)
        
        assert found is loan


class TestRepositoryFindByUser:
    """Test suite for findByUser operations"""

    def test_find_by_user_single_loan(self):
        """Test finding loans for user with one loan"""
        repo = InMemoryLoanRepository()
        book_id = BookId(uuid4())
        user_id = UserId(uuid4())
        loan = Loan(book_id, user_id)
        
        repo.save(loan)
        loans = repo.findByUser(user_id.value)
        
        assert len(loans) == 1
        assert loans[0] == loan

    def test_find_by_user_multiple_loans(self):
        """Test finding multiple loans for same user"""
        repo = InMemoryLoanRepository()
        user_id = UserId(uuid4())
        
        loan1 = Loan(BookId(uuid4()), user_id)
        loan2 = Loan(BookId(uuid4()), user_id)
        loan3 = Loan(BookId(uuid4()), user_id)
        
        repo.save(loan1)
        repo.save(loan2)
        repo.save(loan3)
        
        loans = repo.findByUser(user_id.value)
        
        assert len(loans) == 3
        assert loan1 in loans
        assert loan2 in loans
        assert loan3 in loans

    def test_find_by_user_no_loans(self):
        """Test finding loans for user with no loans"""
        repo = InMemoryLoanRepository()
        user_id = UserId(uuid4())
        
        loans = repo.findByUser(user_id.value)
        
        assert loans == []

    def test_find_by_user_with_user_id_object(self):
        """Test finding loans with UserId object"""
        repo = InMemoryLoanRepository()
        user_id = UserId(uuid4())
        loan = Loan(BookId(uuid4()), user_id)
        
        repo.save(loan)
        loans = repo.findByUser(user_id)
        
        assert len(loans) == 1

    def test_find_by_user_filters_correctly(self):
        """Test that findByUser only returns loans for specified user"""
        repo = InMemoryLoanRepository()
        user1_id = UserId(uuid4())
        user2_id = UserId(uuid4())
        
        loan1 = Loan(BookId(uuid4()), user1_id)
        loan2 = Loan(BookId(uuid4()), user2_id)
        
        repo.save(loan1)
        repo.save(loan2)
        
        user1_loans = repo.findByUser(user1_id.value)
        
        assert len(user1_loans) == 1
        assert user1_loans[0] == loan1


class TestRepositoryListAll:
    """Test suite for list_all operations"""

    def test_list_all_empty(self):
        """Test listing all loans when repository is empty"""
        repo = InMemoryLoanRepository()
        
        all_loans = repo.list_all()
        
        assert all_loans == []

    def test_list_all_single_loan(self):
        """Test listing all loans with one loan"""
        repo = InMemoryLoanRepository()
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        
        repo.save(loan)
        all_loans = repo.list_all()
        
        assert len(all_loans) == 1
        assert all_loans[0] == loan

    def test_list_all_multiple_loans(self):
        """Test listing all loans with multiple loans"""
        repo = InMemoryLoanRepository()
        
        loans = [
            Loan(BookId(uuid4()), UserId(uuid4())),
            Loan(BookId(uuid4()), UserId(uuid4())),
            Loan(BookId(uuid4()), UserId(uuid4()))
        ]
        
        for loan in loans:
            repo.save(loan)
        
        all_loans = repo.list_all()
        
        assert len(all_loans) == 3
        for loan in loans:
            assert loan in all_loans

    def test_list_all_returns_list(self):
        """Test that list_all returns a list"""
        repo = InMemoryLoanRepository()
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        
        repo.save(loan)
        all_loans = repo.list_all()
        
        assert isinstance(all_loans, list)


class TestRepositoryIsolation:
    """Test suite for repository isolation"""

    def test_repository_isolation(self):
        """Test that separate repository instances are isolated"""
        repo1 = InMemoryLoanRepository()
        repo2 = InMemoryLoanRepository()
        
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        
        repo1.save(loan)
        
        assert loan.loanId in [l.loanId for l in repo1.list_all()]
        assert loan.loanId not in [l.loanId for l in repo2.list_all()]

    def test_save_multiple_loans_different_users(self):
        """Test saving loans for different users"""
        repo = InMemoryLoanRepository()
        
        user1 = UserId(uuid4())
        user2 = UserId(uuid4())
        
        loan1 = Loan(BookId(uuid4()), user1)
        loan2 = Loan(BookId(uuid4()), user2)
        
        repo.save(loan1)
        repo.save(loan2)
        
        assert len(repo.list_all()) == 2
        assert len(repo.findByUser(user1.value)) == 1
        assert len(repo.findByUser(user2.value)) == 1


class TestRepositoryEdgeCases:
    """Test suite for repository edge cases"""

    def test_find_by_id_empty_repository(self):
        """Test findById on empty repository"""
        repo = InMemoryLoanRepository()
        result = repo.findById(uuid4())
        assert result is None

    def test_find_by_user_empty_repository(self):
        """Test findByUser on empty repository"""
        repo = InMemoryLoanRepository()
        result = repo.findByUser(uuid4())
        assert result == []

    def test_data_structure_integrity(self):
        """Test that internal data structure remains dict"""
        repo = InMemoryLoanRepository()
        loan = Loan(BookId(uuid4()), UserId(uuid4()))
        
        repo.save(loan)
        
        assert isinstance(repo.data, dict)
        assert str(loan.loanId) in repo.data