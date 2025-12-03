# domain/loan.py
from uuid import uuid4, UUID
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
        self.createdAt = datetime.utcnow()
        self.dueDate = None
        self.verified = False #mastiin udah ke verifikasi admin
        self.approved = False #mastiin pinjaman udah di acc admin
        self.return_initiated = False #menandai peminjaman sudah mulai proses pengembalian
        self.return_verified = False #menandai bahwa admin udh ngecek & verify kondisi buku 

    # borrower action: kondisi buku bener2 dipinjem
    def borrow(self, due_date: DueDate):
        self.loanStatus = LoanStatus.BORROWED #status berubah jadi dipinjem
        self.dueDate = due_date 
        self.verified = True
        self.approved = True
        self.return_initiated = False

    # admin verifies request (checks business rules)
    def verify(self):
        if self.loanStatus != LoanStatus.REQUESTED:
            raise ValueError("Loan is not in requested state")
        self.verified = True

    # admin approves (distribute)
    def approve(self, due_date: DueDate):
        if not self.verified:
            raise ValueError("Loan must be verified before approval")
        self.approved = True
        self.loanStatus = LoanStatus.BORROWED
        self.dueDate = due_date
        self.createdAt = datetime.utcnow()

    # borrower mulai proses pengembalian
    def initiate_return(self):
        if self.loanStatus != LoanStatus.BORROWED:
            raise ValueError("Loan is not currently borrowed")
        self.return_initiated = True #masuk ke step pengembalian
        # status tetap borowed sampai admin verifikasi

    # admin memfinalisasi pengembalian
    def finalize_return(self):
        if not self.return_initiated:
            raise ValueError("Return not initiated")
        self.return_verified = True
        self.loanStatus = LoanStatus.RETURNED
        self.return_initiated = False
        self.dueDate = None

    def mark_overdue(self): 
        #menandai pinjaman sebagai terlambat
        self.loanStatus = LoanStatus.OVERDUE

    def extend_loan(self, extra_days: int):
        if not self.dueDate:
            raise ValueError("No due date to extend")
        new_date = self.dueDate.value + timedelta(days=extra_days)
        self.dueDate = DueDate(new_date)
        return self.dueDate
