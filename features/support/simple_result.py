class SimpleResult:
    def __init__(self, value):
        self.value = value

    def get_result(self, unused):
        return SimpleResult(self.value)

    def get_value(self):
        return self.value
