from random import randint
from time import clock


        
# class Transition(object):
#     def __init__(self, toState):
#         self.toState = toState
#         
#     def execute(self):
#         print('Transitioning...')
#         
# class Attack(State):
#     def __init__(self):
#         super(Attack, self).__init__()
# 
#     def enter(self):
#             print("Starting to Attack")
#             super().enter()
#             
#     def execute(self):
#             print("Attacking")
#             if (self.startTime +self.timer <= clock()):
#                 if not(randint(1,2) %2):
#                    self.FSM.toTransition("toFollow")
# 
#         
#     def exit(self):
#             print ("Finished Attacking")
    
# class StateMachine(object):
#     def __init__ (self, character):
#         self.char = character
#         self.states = {}
#         self.transitions = {}
#         self.currState = None
#         self.prevState = None
#         self.trans  = None
#         
#     def addTransition(self, transName, transition):
#         self.transitions[transName] = transition
#         
#     def addState(self, stateName, state):
#         self.states[stateName] = state
#     
#     def setState(self, stateName):
#         self.prevState = self.currState
#         self.currState = self.states[stateName]
#     
#     def toTransition(self, toTrans):
#         self.trans = self.transitions[toTrans]
#     
#     def execute(self):
#         if self.trans:
#             self.currState.exit()
#             self.trans.execute()
#             self.setState(self.trans.toState)
#             self.currState.enter()
#             self.trans = None
#         self.currState.execute()
    
         
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
    
    
class Idle(State):
    def __init__(self):
        super(Idle, self).__init__()
        self.name = "Idle" 
        
    def transition_in(self):
            print("Preparing to Idle.")
            super().enter()
            
    def execute(self):
            print("Idle")
            if randint(0,1) :
                self.nextState = "Follow"

                    
    def transition_out(self):
            print ("Finished Idling")
            
            

            
class Follow(State):
    def __init__(self):
        super(Follow, self).__init__()
        self.name = "Follow"

    def transition_in(self):
        print("Starting to Follow")
        super().enter()
            
    def execute(self):
        print("Following")
            if randint(0,1):
                self.nextState = "Idle"
        
    def transition_out(self):
        print ("Done Following")
        


class NPC(object):
    def __init__(self):
        self.state = Idle()
        self.nextState = None
        
    def update(self):
        self.state.execute()
        print(self.nextState)
        


if __name__ == "__main__":
    state_dict = {  "Idle": Idle(),
                    "Follow": Follow()}
    c= NPC()
    c.state_dict = state_dict
    
    for i in range(20):
        startTime = clock()
        timeInterval = 1
        while (startTime +timeInterval > clock()):
            pass
        c.update()

        
        
        
        
                