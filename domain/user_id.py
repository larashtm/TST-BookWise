from uuid import UUID

class UserId:
    def __init__(self, value: UUID):
        if value is None:
            raise TypeError("UserId requires UUID, got None")
        if not isinstance(value, UUID):
            raise TypeError(f"UserId requires UUID, got {type(value).__name__}")
        self.value = value