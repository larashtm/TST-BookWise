import pytest
from datetime import date, timedelta
from domain.loan_policy_service import LoanPolicyService
from domain.due_date import DueDate


class TestLoanPolicyServiceBasic:
    """Test suite for basic LoanPolicyService functionality"""

    def test_calculate_due_date_returns_due_date(self):
        """Test that calculate_due_date returns a DueDate object"""
        service = LoanPolicyService()
        due_date = service.calculate_due_date()
        
        assert isinstance(due_date, DueDate)
        assert due_date.value is not None

    def test_calculate_due_date_is_7_days_future(self):
        """Test that calculated due date is 7 days from today"""
        service = LoanPolicyService()
        expected_date = date.today() + timedelta(days=7)
        
        due_date = service.calculate_due_date()
        
        assert due_date.value == expected_date

    def test_calculate_due_date_not_overdue(self):
        """Test that newly calculated due date is not overdue"""
        service = LoanPolicyService()
        due_date = service.calculate_due_date()
        
        assert due_date.is_overdue() is False


class TestLoanPolicyServiceConsistency:
    """Test suite for LoanPolicyService consistency"""

    def test_calculate_due_date_multiple_calls(self):
        """Test that multiple calls return consistent results for same day"""
        service = LoanPolicyService()
        
        due_date1 = service.calculate_due_date()
        due_date2 = service.calculate_due_date()
        
        assert due_date1.value == due_date2.value

    def test_calculate_due_date_consistent_across_day(self):
        """Test that due date remains consistent for same day calculations"""
        service = LoanPolicyService()
        today = date.today()
        expected = today + timedelta(days=7)
        
        results = [service.calculate_due_date() for _ in range(5)]
        
        for due_date in results:
            assert due_date.value == expected


class TestLoanPolicyServiceInstances:
    """Test suite for multiple LoanPolicyService instances"""

    def test_service_can_be_instantiated_multiple_times(self):
        """Test that multiple service instances work independently"""
        service1 = LoanPolicyService()
        service2 = LoanPolicyService()
        
        due_date1 = service1.calculate_due_date()
        due_date2 = service2.calculate_due_date()
        
        assert due_date1.value == due_date2.value

    def test_service_stateless(self):
        """Test that service is stateless and doesn't retain calculations"""
        service = LoanPolicyService()
        
        first_call = service.calculate_due_date()
        second_call = service.calculate_due_date()
        
        # Both should return the same date if called on the same day
        assert first_call.value == second_call.value
        
        # Service should not have any stored state
        assert not hasattr(service, 'last_calculated')
        assert not hasattr(service, '_cached_date')


class TestLoanPolicyServiceValidation:
    """Test suite for LoanPolicyService validation"""

    def test_calculate_due_date_value_type(self):
        """Test that the value in DueDate is of date type"""
        service = LoanPolicyService()
        due_date = service.calculate_due_date()
        
        assert isinstance(due_date.value, date)

    def test_policy_7_day_rule(self):
        """Test that the 7-day policy rule is enforced"""
        service = LoanPolicyService()
        due_date = service.calculate_due_date()
        
        delta = due_date.value - date.today()
        assert delta.days == 7


class TestLoanPolicyServiceEdgeCases:
    """Test suite for LoanPolicyService edge cases"""

    def test_service_initialization(self):
        """Test that service can be initialized without parameters"""
        service = LoanPolicyService()
        assert service is not None

    def test_due_date_always_future(self):
        """Test that calculated due date is always in the future"""
        service = LoanPolicyService()
        due_date = service.calculate_due_date()
        
        assert due_date.value > date.today()

    def test_multiple_services_independent(self):
        """Test that multiple service instances are independent"""
        services = [LoanPolicyService() for _ in range(3)]
        due_dates = [s.calculate_due_date() for s in services]
        
        # All should return the same date
        assert all(dd.value == due_dates[0].value for dd in due_dates)