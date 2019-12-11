class PickleNames:
    def __init__(self, basename):
        self.basename = basename

    @property
    def hashed(self):
        return f"hashed_{self.basename}"

    @property
    def n2v_embedded(self):
        return f"n2v_embedded_{self.basename}"
