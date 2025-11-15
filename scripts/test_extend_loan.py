# scripts/test_extend_loan.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain.loan import Loan
from domain.book_id import BookId
from domain.user_id import UserId
from domain.due_date import DueDate
from datetime import datetime
import traceback
b = BookId('b1')
u = UserId('u1')
loan = Loan(b, u)
loan.dueDate = DueDate(datetime.now())

print("Before extend:", loan.dueDate.value, type(loan.dueDate.value))

try:
    loan.extend_loan(7)
    print("After extend:", loan.dueDate.value, type(loan.dueDate.value))
except Exception:
    traceback.print_exc()