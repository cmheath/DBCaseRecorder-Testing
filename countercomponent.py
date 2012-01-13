# --- Inherent python/system level imports

# --- OpenMDAO imports
from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Int
     
class CounterComp(Component): 
       
    # --- Initialize counter variable ---
    config = Int(0, iotype = 'out', desc ='current design configuration number')
      
    def __init__(self, *args, **kwargs):
        # ---------------------------------------------
        # --- Constructor for the counter component ---
        # ---------------------------------------------
        super(CounterComp, self).__init__(*args, **kwargs)      
        self.config = 1
        
        self.force_execute = True    
        
    def execute(self): 
        
        self.config = self.config + 1                               
            
if __name__ == "__main__":
    
    # --- Default test case ---      
   c = CounterComp()
