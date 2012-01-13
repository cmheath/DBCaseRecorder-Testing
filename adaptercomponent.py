# --- Inherent python/system level imports
import math

# --- OpenMDAO imports
from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, Int
     
class AdapterComp(Component): 
    
    # --- Geometry-based design parameters ---
    vane_num = Float(6, low = 4, high = 8, iotype ='in', desc ='number of vane blades per injector element')
    injector_loc = Float(0.0, low = 0.0, high = 1.0, iotype ='in', desc ='location of injetor tip relative to venturi throat')
    injector_dia = Float(0.0, low = 0.0, high = 1.0, iotype ='in', desc ='outer diameter of each fuel module - indirectly controls injector #', units = 'inch')
    
    # --- Initialize output variables ---
    vane_num_out = Int(6, iotype = 'out')
    injector_loc_out = Float(0.0, iotype = 'out')
    injector_dia_out = Float(0.0, iotype = 'out')
    num_injectors = Int(0, iotype = 'out')
      
    # --- Specify constants ---
    area_eff = 7*math.pi*(0.8/2.0)**2 # --- Effective area of 7-pt injector array (baseline) --- Keep this area constant for all configurations
    
    def execute(self): 
        
        print 'run adapter'
        self.vane_num_out = int(round(self.vane_num))
        
        if self.injector_dia <= 1.0/3.0:
            self.injector_dia_out = 2*(math.sqrt(self.area_eff/(math.pi*19)))     # --- 19 Point LDI Configuration
            self.num_injectors = 19
        elif (self.injector_dia > 1.0/3.0) and (self.injector_loc <= 2.0/3.0):
            self.injector_dia_out = 2*(math.sqrt(self.area_eff/(math.pi*7)))      # --- 7 Point LDI Configuration
            self.num_injectors = 7
        else:
            self.injector_dia_out = 2*(math.sqrt(self.area_eff/(math.pi*1)))      # --- 1 Point LDI Configuration
            self.num_injectors = 1
        
        if self.injector_loc <= (1.0/3.0):
            self.injector_loc_out = 1.0                                              # --- Inside Venturi Throat
        elif (self.injector_loc > (1.0/3.0)) and (self.injector_loc <= 2.0/3.0):
            self.injector_loc_out = 1.05                                             # --- Even With Venturi Throat
        else:
            self.injector_loc_out = 1.1                                              # --- Outside Venturi Throat

