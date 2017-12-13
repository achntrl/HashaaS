import hashlib


class AbstractHasher:
    def __init__(self, data=None, iterations=None):
        self.data = data
        self.iterations = iterations

    def hash(self):
        raise NotImplementedError


class DummyHasher(AbstractHasher):
    def hash(self):
        return "00000000000000000"


class Md5Hasher(AbstractHasher):
    def hash(self):
        data = self.data
        for i in range(self.iterations):
            data = hashlib.md5(data.encode('utf-8')).hexdigest()

        return data

class Sha1Hasher(AbstractHasher):
    def hash(self):
        data = self.data
        for i in range(self.iterations):
            data = hashlib.sha1(data.encode('utf-8')).hexdigest()

        return data

class Sha256Hasher(AbstractHasher):
    def hash(self):
        data = self.data
        for i in range(self.iterations):
            data = hashlib.sha256(data.encode('utf-8')).hexdigest()

        return data
