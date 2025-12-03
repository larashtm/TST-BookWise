from pydantic import BaseModel
from uuid import UUID
from typing import Optional
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
    dueDate: Optional[date] = None
    verified: Optional[bool] = False
    approved: Optional[bool] = False
    return_initiated: Optional[bool] = False
