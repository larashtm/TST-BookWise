from domain.loan_repository import LoanRepository

class InMemoryLoanRepository(LoanRepository):
    def __init__(self):
        self.data = {}

    def save(self, loan):
        self.data[loan.loanId] = loan

    def findById(self, id):
        return self.data.get(id)

    def findByUser(self, user_id):
        return [
            loan for loan in self.data.values()
            if loan.userId.value == user_id.value
        ]
