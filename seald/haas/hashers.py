class AbstractHasher:
    def __init__(self, data=None):
        self.data = data

    def hash(self):
        raise NotImplementedError


class DummyHasher(AbstractHasher):
    def hash(self):
        return "00000000000000000"
