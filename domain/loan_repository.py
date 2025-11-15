from abc import ABC, abstractmethod
from uuid import UUID

class LoanRepository(ABC):

    @abstractmethod
    def save(self, loan):
        pass

    @abstractmethod
    def findById(self, id: UUID):
        pass

    @abstractmethod
    def findByUser(self, user_id):
        pass
