from datetime import date

class DueDate:
    def __init__(self, value: date):
        if not isinstance(value, date):
            raise TypeError(f"DueDate requires date, got {type(value)}")
        self.value = value

    def is_overdue(self):
        return date.today() > self.value