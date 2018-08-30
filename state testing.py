from random import randint
from time import clock


         
class State(object):
    def __init__(self):
        self.timer = 0
        self.startTime = 0
        
    def transition_in(self):
        self.timer = randint(0,5)
        self.startTime = int(clock())
        
    def execute(self):
        pass
        
    def transition_out(self):
        pass
    

class NPC(object):
    def __init__(self):
        self.FSM = []
        
    def update(self):
        self.FSM.append(State())
        


n = NPC()
        
                