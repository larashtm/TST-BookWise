from uuid import uuid4
from datetime import datetime, timedelta
from domain.loan_status import LoanStatus
from domain.book_id import BookId
from domain.user_id import UserId
from domain.due_date import DueDate
 

class Loan:
    def __init__(self, bookId: BookId, userId: UserId):
        self.loanId = uuid4()
        self.bookId = bookId
        self.userId = userId
        self.loanStatus = LoanStatus.REQUESTED
        self.createdAt = datetime.now()
        self.dueDate = None

    def borrow(self, due_date: DueDate):
        self.loanStatus = LoanStatus.BORROWED
        self.dueDate = due_date

    def return_book(self):
        self.loanStatus = LoanStatus.RETURNED

    def mark_overdue(self):
        self.loanStatus = LoanStatus.OVERDUE

    def extend_loan(self, extra_days: int):
        if self.dueDate:
            new_date = self.dueDate.value + timedelta(days=extra_days)
            self.dueDate = DueDate(new_date)
