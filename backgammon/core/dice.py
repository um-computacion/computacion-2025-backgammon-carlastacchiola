import random 

class dice:
    def __init__(self):
        self.values = []

    def roll_single(self):
        value = random.randint(1,6)
        self.values = [value]
        return value
    
    
    def roll(self):
        self.values = [random.randint(1, 6), random.randint(1, 6)]
        return self.values


    