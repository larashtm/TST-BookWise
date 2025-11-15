from datetime import date, timedelta
from domain.due_date import DueDate

class LoanPolicyService:
    def calculate_due_date(self):
        return DueDate(date.today() + timedelta(days=7))
