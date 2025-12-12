from uuid import UUID

class BookId:
    def __init__(self, value: UUID):
        if value is None:
            raise TypeError("BookId requires UUID, got None")
        if not isinstance(value, UUID):
            raise TypeError(f"BookId requires UUID, got {type(value).__name__}")
        self.value = value