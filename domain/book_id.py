from uuid import UUID

class BookId:
    def __init__(self, value: UUID):
        if not isinstance(value, UUID):
            raise TypeError(f"BookId requires UUID, got {type(value)}")
        self.value = value