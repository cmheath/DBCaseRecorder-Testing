''' Top level assembly for the Lean Direct Injection (LDI) design space analysis '''

# --- Inherent python/system level imports
import os
import math
import sys
import logging

# --- OpenMDAO main and library imports
from openmdao.main.api import Assembly, SequentialWorkflow, enable_console, set_as_top
from openmdao.lib.drivers.api import DOEdriver, BroydenSolver
from openmdao.lib.doegenerators.api import OptLatinHypercube
#from openmdao.lib.casehandlers.api import DBCaseRecorder,  case_db_to_dict
from openmdao.lib.casehandlers.db import DBCaseIterator, DBCaseRecorder, case_db_to_dict

# --- OpenMDAO component imports
from countercomponent import CounterComp
from adaptercomponent import AdapterComp
from geometrycomponent import GeometryComp
from pathname import Path
from run_local import run_local

DOE_OUT_DB = 'DOE_Output.db'

class Analysis(Assembly):
    ''' Top level for the Lean Direct Injection (LDI) combustion design space analysis '''
    def __init__(self):
        super(Analysis, self).__init__()
        
        # --------------------------------------------------------------------------- #
        # --- Instantiate LHC DOE Driver
        # --------------------------------------------------------------------------- #  
        self.add('doe_driver', DOEdriver())       
        self.doe_driver.DOEgenerator = OptLatinHypercube(num_samples = 10)
        self.doe_driver.workflow = SequentialWorkflow()
        
        # --------------------------------------------------------------------------- #
        # --- Instantiate LHC Adapter Component
        # --- Modifies LHC to convert continuous design variable to discrete
        # --------------------------------------------------------------------------- #          
        self.add('adapter', AdapterComp())
       
        # --------------------------------------------------------------------------- #
        # --- Instantiate Geometry Component
        # --------------------------------------------------------------------------- #  
        self.add('geometry', GeometryComp()) 

        # 1--- Top Level Workflow
        self.driver.workflow.add(['doe_driver']) 
        self.doe_driver.workflow.add(['adapter', 'geometry'])
    
        # --------------------------------------------------------------------------- #
        # --- Add parameters to DOE driver 
        # --------------------------------------------------------------------------- #         
        self.doe_driver.add_parameter('adapter.vane_num')
        self.doe_driver.add_parameter('adapter.injector_loc')
        self.doe_driver.add_parameter('adapter.injector_dia')
        self.doe_driver.add_parameter('geometry.vane_pitch')
        self.doe_driver.add_parameter('geometry.venturi_angle')

        # --------------------------------------------------------------------------- #        
        # Specify DBcaseRecorder for DOE 
        # --------------------------------------------------------------------------- #            
        self.doe_driver.case_outputs = ['adapter.vane_num_out', 'adapter.injector_loc_out', 'adapter.injector_dia_out', 'geometry.vane_num', 'geometry.injector_loc', 'geometry.injector_dia']        
        self.doe_driver.recorder = DBCaseRecorder(DOE_OUT_DB) 
        
        #self.add('DOE_restart', DBCaseIterator(DOE_OUT_DB))
   
        # --------------------------------------------------------------------------- #
        # --- Specify Non-NPSS Data Connections 
        # --------------------------------------------------------------------------- #  
        self.connect('adapter.vane_num_out', 'geometry.vane_num')
        self.connect('adapter.injector_loc_out', 'geometry.injector_loc')
        self.connect('adapter.injector_dia_out', 'geometry.injector_dia')

        
if __name__ == '__main__':
    
    try: 
        os.remove(DOE_OUT_DB)
    except OSError:
        pass
        
    top_level_analysis = set_as_top(Analysis())  
    top_level_analysis.run()    
    
    vars = ['adapter.vane_num_out','adapter.injector_loc_out','adapter.injector_dia_out','geometry.vane_num','geometry.injector_loc', 'geometry.injector_dia']  
    doe_designs = case_db_to_dict(DOE_OUT_DB, vars)
    print doe_designs

    for k,v in doe_designs.iteritems(): 
        print k,v
           
    print top_level_analysis.doe_driver.recorder
    
    data = top_level_analysis.doe_driver.recorder.get_iterator()
    inputs = [case['adapter.vane_num_out'] for case in data]
    print inputs
              


    exit()

    # --------------------------------END---------------------------------------- #        
        

    

       