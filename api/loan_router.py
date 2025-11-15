from fastapi import APIRouter, HTTPException
from uuid import UUID

from domain.loan import Loan
from domain.book_id import BookId
from domain.user_id import UserId
from domain.loan_policy_service import LoanPolicyService
from infrastructure.in_memory_loan_repository import InMemoryLoanRepository
from schemas.loan_schema import LoanCreateRequest, LoanResponse

router = APIRouter()
repo = InMemoryLoanRepository()
policy = LoanPolicyService()


@router.post("/loans", response_model=LoanResponse)
def create_loan(req: LoanCreateRequest):
    loan = Loan(BookId(req.bookId), UserId(req.userId))
    due = policy.calculate_due_date()
    loan.borrow(due)

    repo.save(loan)

    return LoanResponse(
        loanId=loan.loanId,
        bookId=loan.bookId.value,
        userId=loan.userId.value,
        status=loan.loanStatus.value,     # <- FIX
        createdAt=loan.createdAt,
        dueDate=loan.dueDate.value
    )


@router.get("/loans/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: UUID):              # <- FIX (UUID type)
    loan = repo.findById(loan_id)

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    return LoanResponse(
        loanId=loan.loanId,
        bookId=loan.bookId.value,
        userId=loan.userId.value,
        status=loan.loanStatus.value,     # <- FIX
        createdAt=loan.createdAt,
        dueDate=loan.dueDate.value
    )
