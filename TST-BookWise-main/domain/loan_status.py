from enum import Enum

class LoanStatus(str, Enum):
    REQUESTED = "requested"
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"
