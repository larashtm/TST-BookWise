import pytest
from datetime import date, timedelta
from domain.due_date import DueDate


class TestDueDateCreation:
    """Test suite for DueDate creation"""

    def test_create_due_date_with_valid_date(self):
        """Test creating DueDate with valid date"""
        today = date.today()
        due_date = DueDate(today)
        assert due_date.value == today

    def test_create_due_date_future(self):
        """Test creating DueDate with future date"""
        future_date = date.today() + timedelta(days=7)
        due_date = DueDate(future_date)
        assert due_date.value == future_date

    def test_create_due_date_past(self):
        """Test creating DueDate with past date"""
        past_date = date.today() - timedelta(days=7)
        due_date = DueDate(past_date)
        assert due_date.value == past_date


class TestDueDateOverdue:
    """Test suite for DueDate overdue checking"""

    def test_is_overdue_with_past_date(self):
        """Test is_overdue returns True for past dates"""
        past_date = date.today() - timedelta(days=1)
        due_date = DueDate(past_date)
        assert due_date.is_overdue() is True

    def test_is_overdue_with_future_date(self):
        """Test is_overdue returns False for future dates"""
        future_date = date.today() + timedelta(days=7)
        due_date = DueDate(future_date)
        assert due_date.is_overdue() is False

    def test_is_overdue_with_today(self):
        """Test is_overdue returns False for today's date"""
        today = date.today()
        due_date = DueDate(today)
        assert due_date.is_overdue() is False

    def test_is_overdue_edge_case_yesterday(self):
        """Test is_overdue for yesterday's date"""
        yesterday = date.today() - timedelta(days=1)
        due_date = DueDate(yesterday)
        assert due_date.is_overdue() is True


class TestDueDateValidation:
    """Test suite for DueDate validation"""

    def test_due_date_with_none_raises_error(self):
        """Test that creating DueDate with None raises error"""
        with pytest.raises((TypeError, AttributeError)):
            DueDate(None)

    def test_due_date_with_string_raises_error(self):
        """Test that creating DueDate with string raises error"""
        with pytest.raises((TypeError, AttributeError)):
            DueDate("2025-12-31")

    def test_due_date_with_integer_raises_error(self):
        """Test that creating DueDate with integer raises error"""
        with pytest.raises((TypeError, AttributeError)):
            DueDate(20251231)


class TestDueDateComparison:
    """Test suite for DueDate comparison operations"""

    def test_due_date_equality(self):
        """Test equality between DueDate instances"""
        target_date = date.today() + timedelta(days=7)
        due_date1 = DueDate(target_date)
        due_date2 = DueDate(target_date)
        assert due_date1.value == due_date2.value

    def test_due_date_inequality(self):
        """Test inequality between different DueDate instances"""
        due_date1 = DueDate(date.today())
        due_date2 = DueDate(date.today() + timedelta(days=1))
        assert due_date1.value != due_date2.value

    def test_due_date_comparison(self):
        """Test comparison between DueDate values"""
        earlier = DueDate(date.today())
        later = DueDate(date.today() + timedelta(days=7))
        assert earlier.value < later.value


class TestDueDateEdgeCases:
    """Test suite for DueDate edge cases"""

    def test_due_date_one_year_future(self):
        """Test DueDate with date one year in the future"""
        future = date.today() + timedelta(days=365)
        due_date = DueDate(future)
        assert due_date.value == future
        assert not due_date.is_overdue()

    def test_due_date_specific_date(self):
        """Test creating DueDate with specific date"""
        specific = date(2025, 12, 31)
        due_date = DueDate(specific)
        assert due_date.value == specific

    def test_due_date_far_past(self):
        """Test DueDate with date far in the past"""
        far_past = date.today() - timedelta(days=365)
        due_date = DueDate(far_past)
        assert due_date.is_overdue() is True

    def test_due_date_immutability(self):
        """Test that DueDate value remains constant"""
        target_date = date.today() + timedelta(days=7)
        due_date = DueDate(target_date)
        assert due_date.value == target_date
        # Multiple accesses should return same value
        assert due_date.value == target_date