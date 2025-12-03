from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List
from pydantic import BaseModel

from domain.loan import Loan
from domain.book_id import BookId
from domain.user_id import UserId
from domain.loan_policy_service import LoanPolicyService
from infrastructure.in_memory_loan_repository import InMemoryLoanRepository
from schemas.loan_schema import LoanCreateRequest, LoanResponse
from auth.deps import require_role, allow_roles

router = APIRouter(prefix="", tags=["Loans"])

repo = InMemoryLoanRepository()
policy = LoanPolicyService()

# ----------------------------
# Helper convert Loan → dict
# ----------------------------
def to_response(loan: Loan) -> dict:
    return {
        "loanId": loan.loanId,
        "bookId": loan.bookId.value,
        "userId": loan.userId.value,
        "status": loan.loanStatus.value,
        "createdAt": loan.createdAt,
        "dueDate": loan.dueDate.value if loan.dueDate else None,
        "verified": getattr(loan, "verified", False),
        "approved": getattr(loan, "approved", False),
        "return_initiated": getattr(loan, "return_initiated", False),
    }

# ================================================================
# 1. CREATE LOAN — PEMINJAM
# ================================================================
@router.post("/loans", response_model=LoanResponse, status_code=201)
def create_loan(req: LoanCreateRequest, current_user=Depends(require_role("peminjam"))):
    loan = Loan(BookId(req.bookId), UserId(req.userId))
    repo.save(loan)
    return to_response(loan)

# ================================================================
# 2. LIST MY LOANS — PEMINJAM
# ================================================================
@router.get("/loans/my", response_model=List[LoanResponse])
def list_my_loans(current_user=Depends(require_role("peminjam"))):
    user = current_user
    loans = repo.findByUser(user.user_id)
    return [to_response(l) for l in loans]

# ================================================================
# 3. LIST ALL LOANS — PENGGUNA
# ================================================================
@router.get("/loans/all", response_model=List[LoanResponse])
def list_all_loans(current_user=Depends(require_role("pengguna"))):
    loans = repo.list_all()
    return [to_response(l) for l in loans]

# ================================================================
# 4. GET LOAN BY ID — PEMINJAM / PENGGUNA
# ================================================================
@router.get("/loans/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: UUID, current_user=Depends(allow_roles("peminjam", "pengguna"))):
    loan = repo.findById(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    user = current_user
    if user.role == "peminjam" and str(loan.userId.value) != str(user.user_id):
        raise HTTPException(status_code=403, detail="Forbidden")
    return to_response(loan)

# ================================================================
# 5. VERIFY LOAN — PENGGUNA
# ================================================================
@router.post("/loans/{loan_id}/verify")
def verify_loan(loan_id: UUID, current_user=Depends(require_role("pengguna"))):
    loan = repo.findById(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    try:
        loan.verify()
        repo.save(loan)
        return {"detail": "Loan verified"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ================================================================
# 6. APPROVE LOAN — PENGGUNA
# ================================================================
@router.post("/loans/{loan_id}/approve")
def approve_loan(loan_id: UUID, current_user=Depends(require_role("pengguna"))):
    loan = repo.findById(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    try:
        due = policy.calculate_due_date()
        loan.approve(due)
        repo.save(loan)
        return {"detail": "Loan approved", "dueDate": due.value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ================================================================
# 7. INITIATE RETURN — PEMINJAM
# ================================================================
@router.post("/loans/{loan_id}/return")
def initiate_return(loan_id: UUID, current_user=Depends(require_role("peminjam"))):
    loan = repo.findById(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    user = current_user
    if str(loan.userId.value) != str(user.user_id):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        loan.initiate_return()
        repo.save(loan)
        return {"detail": "Return initiated"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ================================================================
# 8. FINALIZE RETURN — PENGGUNA
# ================================================================
@router.post("/loans/{loan_id}/finalize-return")
def finalize_return(loan_id: UUID, current_user=Depends(require_role("pengguna"))):
    loan = repo.findById(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    try:
        loan.finalize_return()
        repo.save(loan)
        return {"detail": "Return finalized"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ================================================================
# 9. EXTEND LOAN — PEMINJAM
# ================================================================
class ExtendRequest(BaseModel):
    extra_days: int

@router.post("/loans/{loan_id}/extend")
def extend_loan(loan_id: UUID, req: ExtendRequest, current_user=Depends(require_role("peminjam"))):
    loan = repo.findById(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    user = current_user
    if str(loan.userId.value) != str(user.user_id):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        new_due = loan.extend_loan(req.extra_days)
        repo.save(loan)
        return {"detail": "Extension applied", "newDueDate": new_due.value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
