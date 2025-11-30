from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from domain.loan import Loan
from domain.book_id import BookId
from domain.user_id import UserId
from domain.loan_policy_service import LoanPolicyService
from infrastructure.in_memory_loan_repository import InMemoryLoanRepository
from schemas.loan_schema import LoanCreateRequest, LoanResponse

from auth.deps import require_role, allow_roles, get_current_active_user

router = APIRouter(prefix="", tags=["Loans"])

repo = InMemoryLoanRepository()
policy = LoanPolicyService()


# ===============================
# 1) TARUH /loans/all DI ATAS !!!
# ===============================
@router.get("/loans/all")
def list_all_loans(current_user = Depends(require_role("pengguna"))):
    loans = repo.data.values()
    return [
        {
            "loanId": l.loanId,
            "bookId": l.bookId.value,
            "userId": l.userId.value,
            "status": l.loanStatus.value,
            "createdAt": l.createdAt,
            "dueDate": l.dueDate.value if l.dueDate else None
        }
        for l in loans
    ]


# ===============================
# 2) Baru GET /loans/{loan_id}
# ===============================
@router.get("/loans/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: UUID, current_user = Depends(allow_roles("peminjam", "pengguna"))):
    loan = repo.findById(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return LoanResponse(
        loanId=loan.loanId,
        bookId=loan.bookId.value,
        userId=loan.userId.value,
        status=loan.loanStatus.value,
        createdAt=loan.createdAt,
        dueDate=loan.dueDate.value if loan.dueDate else None
    )


# ===============================
# 3) POST tetap di bawah
# ===============================
@router.post("/loans", response_model=LoanResponse, status_code=201)
def create_loan(req: LoanCreateRequest, current_user = Depends(require_role("peminjam"))):
    loan = Loan(BookId(req.bookId), UserId(req.userId))
    due = policy.calculate_due_date()
    loan.borrow(due)
    repo.save(loan)
    return LoanResponse(
        loanId=loan.loanId,
        bookId=loan.bookId.value,
        userId=loan.userId.value,
        status=loan.loanStatus.value,
        createdAt=loan.createdAt,
        dueDate=loan.dueDate.value if loan.dueDate else None
    )
