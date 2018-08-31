from random import randint
from time import clock
import math


        
class Transition(object):
    def __init__(self, toState):
        self.toState = toState
        
    def execute(self):
        pass
         
class State(object):
    def __init__(self, FSM):
        self.FSM = FSM
        self.timer = 0
        self.startTime = 0

        
    def transition_in(self):
        self.timer = randint(0,5)
        self.startTime = int(clock())

        
    def execute(self):
        pass
        
    def transition_out(self):
        pass
    
    
class Idle(State):
    def __init__(self, FSM):
        super(Idle, self).__init__(FSM)

    def transition_in(self):
            # print("Preparing to Idle.")
            super().transition_in()
            
    def execute(self):
        # print("Idle")
        dist = math.sqrt((self.FSM.char.world.player.true_pos[0] - self.FSM.char.true_pos[0])**2 + (self.FSM.char.world.player.true_pos[1] - self.FSM.char.true_pos[1])**2)

        if dist <= 300 and self.FSM.char.world.player.faith != 100:
            self.FSM.toTransition("Follow")
                
    def transition_out(self):
           super().transition_out()

class Haul(State):        
    def __init__(self, FSM):
        super(Haul, self).__init__(FSM)

    def transition_in(self):
            super().transition_in()
            
    def execute(self):
            pass
            
    def transition_out(self):
           super().transition_out()     
           
class Work(State):        
    def __init__(self, FSM):
        super(Work, self).__init__(FSM)

    def transition_in(self):
            super().transition_in()
            
    def execute(self):
            pass
            
    def transition_out(self):
           super().transition_out() 

class Sleep(State):        
    def __init__(self, FSM):
        super(Sleep, self).__init__(FSM)

    def transition_in(self):
            super().transition_in()
            
    def execute(self):
            pass
            
    def transition_out(self):
           super().transition_out() 
            
            
            
class Follow(State):
    def __init__(self, FSM):
        super(Follow, self).__init__(FSM)

    def transition_in(self):
        print('Starting to follow')
        super().transition_in()
        self.FSM.char.target = self.FSM.char.world.player
            
    def execute(self):
        
        dist = math.sqrt((self.FSM.char.world.player.true_pos[0] - self.FSM.char.true_pos[0])**2 + (self.FSM.char.world.player.true_pos[1] - self.FSM.char.true_pos[1])**2)

        clock()-self.startTime

        if dist >= 300 and (clock()-self.startTime)>= 2:
            self.FSM.toTransition("Idle")
        
            
    def transition_out(self):
        super().transition_out()
        self.FSM.char.target = None
        pass
        
       
class Attack(State):
    def __init__(self, FSM):
        super(Attack, self).__init__(FSM)

    def transition_in(self):

        super().transition_in()
            
    def execute(self):
        rand = randint(1,3)
        if rand ==3:
            self.FSM.toTransition("Follow")
            
    def transition_out(self):
        pass      
    
    
class FSM(object):
    def __init__ (self, character):
        self.char = character
        self.states = {}
        self.transitions = {}
        self.currState = None
        self.prevState = None
        self.trans  = None
        
        self.addState("Idle", Idle(self))
        self.addState("Follow", Follow(self))
        self.addState("Attack", Attack(self))
        self.addState("Haul", Haul(self))
        self.addState("Work", Work(self))
        self.addState("Sleep", Sleep(self))
        
        self.addTransition("Idle", Transition("Idle"))
        self.addTransition("Follow", Transition("Follow"))
        self.addTransition("Attack", Transition("Attack"))
        self.addTransition("Haul", Transition("Haul"))
        self.addTransition("Work", Transition("Work"))
        self.addTransition("Sleep", Transition("Sleep"))
        
    def addTransition(self, transName, transition):
        self.transitions[transName] = transition
        
    def addState(self, stateName, state):
        self.states[stateName] = state
    
    def setState(self, stateName):
        self.prevState = self.currState
        self.currState = self.states[stateName]
    
    def toTransition(self, toTrans):
        self.trans = self.transitions[toTrans]
    
    def execute(self):
        if self.trans:
            self.currState.transition_out()
            self.trans.execute()
            self.setState(self.trans.toState)
            self.currState.transition_in()
            self.trans = None
        self.currState.execute()
        
                