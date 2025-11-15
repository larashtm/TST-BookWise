from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date

class LoanCreateRequest(BaseModel):
    bookId: UUID
    userId: UUID

class LoanResponse(BaseModel):
    loanId: UUID
    bookId: UUID
    userId: UUID
    status: str
    createdAt: datetime
    dueDate: date | None = None
