from datetime import date

class DueDate:
    def __init__(self, value: date):
        self.value = value

    def is_overdue(self):
        return date.today() > self.value
