from data.states import  level #, death, shop, levels, battle,
# from data.states import credits
from . import setup, tools
from . import constants as c


LEVEL ='level'
TOWN = 'town'




def main():
    """Add states to control here"""
    
    
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
        
    state_dict = {LEVEL: level.Level(),TOWN: 'town',}
    
    run_it.setup_states(state_dict, c.LEVEL)
    run_it.main()
    
