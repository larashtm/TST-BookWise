from domain.loan_repository import LoanRepository
from uuid import UUID

class InMemoryLoanRepository(LoanRepository):
    def __init__(self): # database palsu
        self.data = {}

    def save(self, loan): # jika udah ada updet 
        self.data[str(loan.loanId)] = loan

    def findById(self, id): # ambil pinjaman berdasarkan id
        # accept either uuid object or string
        key = str(id)
        return self.data.get(key)

    def findByUser(self, user_id):
        uid = str(user_id) if not hasattr(user_id, "value") else str(user_id.value)
        return [
            loan for loan in self.data.values()
            if str(loan.userId.value) == uid
        ]
    
    def list_all(self): #mau kembaliin loan dlm bentuk list
        return list(self.data.values())
