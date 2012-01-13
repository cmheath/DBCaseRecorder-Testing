''' OpenMDAO geometry component '''
''' Updates geometry via the SolidWorks API and exports as a STEP file''' 
''' Loads STEP file into cubit and applies a geometry adaptive tetrahedral mesh'''

# --- Inherent python/system level imports
import os
import sys
import shutil

# --- External python library imports (i.e. matplotlib, numpy, scipy)
from tempfile import TemporaryFile
import math

# --- OpenMDAO imports
from openmdao.main.api import FileMetadata, Component
from openmdao.lib.datatypes.api import Float, Int
from pathname import Path


class GeometryComp(Component):
    ''' OpenMDAO component for Geometry Handling '''
   
    # -----------------------------------------------------
    # --- Initialize Input Design Parameters and Ranges ---
    # -----------------------------------------------------
    vane_num = Int(6, low = 4, high = 8, iotype ='in', desc ='number of vane blades per injector element')
    injector_loc = Float(0.0, iotype ='in', desc ='location of injector tip relative to venturi throat')
    injector_dia = Float(0.0, iotype ='in', desc ='outer diameter of each fuel module - indirectly controls injector # via fill pattern', units = 'inch')
    venturi_angle = Float(45.0, low = 30.0, high = 60.0, iotype ='in', desc ='angle of converging/diverging venturi section', units = 'deg')
    vane_pitch = Float(0.3, low = 0.175, high = 0.35, iotype ='in', desc ='pitch of each helical vane blade')    
        
    def execute(self):
        print 'run_geometry'

        
if __name__ == "__main__":
    
    # -------------------------
    # --- Default Test Case ---
    # ------------------------- 
    Geom_Comp = GeometryComp()
    
    Geom_Comp.run()