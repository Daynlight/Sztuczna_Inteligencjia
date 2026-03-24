class Frame:
    def __init__(self, name):
        self.name = name
        self.slots = {}

    def set(self, key, value):
        self.slots[key] = value

    def get(self, key):
        return self.slots.get(key, None)

    def __repr__(self):
        return f"{self.name}: {self.slots}"