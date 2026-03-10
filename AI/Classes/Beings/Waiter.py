from Classes.Being import Being
from conf import movementSpeed

class Waiter(Being):

    def __init__(self, name, position):
        super().__init__(name, 3, "Assets/jenkins.png", position, movementSpeed, [1,1])

        self.carrying_food = False