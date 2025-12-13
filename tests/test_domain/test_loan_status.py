import pytest
from domain.loan_status import LoanStatus


class TestLoanStatusValues:
    """Test suite for LoanStatus enum values"""

    def test_loan_status_requested_value(self):
        """Test REQUESTED status has correct value"""
        assert LoanStatus.REQUESTED.value == "requested"

    def test_loan_status_borrowed_value(self):
        """Test BORROWED status has correct value"""
        assert LoanStatus.BORROWED.value == "borrowed"

    def test_loan_status_returned_value(self):
        """Test RETURNED status has correct value"""
        assert LoanStatus.RETURNED.value == "returned"

    def test_loan_status_overdue_value(self):
        """Test OVERDUE status has correct value"""
        assert LoanStatus.OVERDUE.value == "overdue"


class TestLoanStatusMembers:
    """Test suite for LoanStatus enum members"""

    def test_loan_status_all_members_exist(self):
        """Test all expected LoanStatus members exist"""
        expected_statuses = {"REQUESTED", "BORROWED", "RETURNED", "OVERDUE"}
        actual_statuses = set(LoanStatus.__members__.keys())
        assert expected_statuses == actual_statuses

    def test_loan_status_member_count(self):
        """Test that LoanStatus has exactly 4 members"""
        assert len(list(LoanStatus)) == 4


class TestLoanStatusComparison:
    """Test suite for LoanStatus comparison operations"""

    def test_loan_status_equality(self):
        """Test equality between same LoanStatus values"""
        status1 = LoanStatus.REQUESTED
        status2 = LoanStatus.REQUESTED
        assert status1 == status2

    def test_loan_status_inequality(self):
        """Test inequality between different LoanStatus values"""
        status1 = LoanStatus.REQUESTED
        status2 = LoanStatus.BORROWED
        assert status1 != status2


class TestLoanStatusCreation:
    """Test suite for LoanStatus creation from string"""

    def test_loan_status_from_string(self):
        """Test creating LoanStatus from string value"""
        status = LoanStatus("requested")
        assert status == LoanStatus.REQUESTED

    def test_loan_status_invalid_string_raises_error(self):
        """Test that invalid string raises ValueError"""
        with pytest.raises(ValueError):
            LoanStatus("invalid_status")


class TestLoanStatusProperties:
    """Test suite for LoanStatus properties"""

    def test_loan_status_is_string_subclass(self):
        """Test that LoanStatus is a string enum"""
        assert isinstance(LoanStatus.REQUESTED, str)
        assert isinstance(LoanStatus.BORROWED.value, str)

    def test_loan_status_name_attribute(self):
        """Test name attribute of LoanStatus"""
        assert LoanStatus.REQUESTED.name == "REQUESTED"
        assert LoanStatus.BORROWED.name == "BORROWED"
        assert LoanStatus.RETURNED.name == "RETURNED"
        assert LoanStatus.OVERDUE.name == "OVERDUE"


class TestLoanStatusOperations:
    """Test suite for LoanStatus operations"""

    def test_loan_status_in_list(self):
        """Test LoanStatus can be used in list operations"""
        statuses = [LoanStatus.REQUESTED, LoanStatus.BORROWED]
        assert LoanStatus.REQUESTED in statuses
        assert LoanStatus.RETURNED not in statuses

    def test_loan_status_iteration(self):
        """Test iterating over LoanStatus values"""
        all_statuses = list(LoanStatus)
        assert len(all_statuses) == 4
        assert LoanStatus.REQUESTED in all_statuses
        assert LoanStatus.BORROWED in all_statuses
        assert LoanStatus.RETURNED in all_statuses
        assert LoanStatus.OVERDUE in all_statuses

    def test_loan_status_string_conversion(self):
        """Test string conversion of LoanStatus"""
        status = LoanStatus.BORROWED
        assert str(status) == "borrowed"

    def test_loan_status_can_be_dict_key(self):
        """Test that LoanStatus can be used as dictionary key"""
        status_dict = {
            LoanStatus.REQUESTED: "Pending approval",
            LoanStatus.BORROWED: "Currently borrowed",
            LoanStatus.RETURNED: "Returned to library"
        }
        assert status_dict[LoanStatus.REQUESTED] == "Pending approval"
        assert status_dict[LoanStatus.BORROWED] == "Currently borrowed"