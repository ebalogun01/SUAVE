## @ingroup Methods-Power-Battery-Sizing
# initialize_from_module_packaging
# 
# Created: Mar 2020, M. Clarke 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from SUAVE.Core import Units
import numpy as np

# ----------------------------------------------------------------------
#  Methods
# ----------------------------------------------------------------------
## @ingroup Methods-Power-Battery-Sizing
def initialize_from_module_packaging(battery):  
    """Calculate pack level properties of battery using cell 
    properties and module configuraton
    
    Assumptions:
    Total battery pack mass contains build-up factor (1.42) for battery casing,
    internal wires, thermal management system and battery management system 
    Factor computed using information of battery properties for X-57 Maxwell 
    Aircraft
    
    Source:
    Cell Charge: Chin, J. C., Schnulo, S. L., Miller, T. B., Prokopius, K., and Gray, 
    J., “Battery Performance Modeling on Maxwell X-57",”AIAA Scitech, San Diego, CA,
    2019. URLhttp://openmdao.org/pubs/chin_battery_performance_x57_2019.pdf.     

    Inputs:
    mass              
    battery.cell
      nominal_capacity    [amp-hours]            
      nominal_voltage     [volts]
      module_config       [unitless]
      mass                [kilograms]
                          
    Outputs:              
     battery.             
       max_energy         [watt-hours]
       max_power          [watts]
       initial_max_energy [watt-hours]
       specific_energy    [watt-hours/kilogram]
       charging_voltage   [volts]
       charging_current   [amps]
       mass_properties.
        mass              [kilograms] 
    """   
    module_weight_factor         = 1.42
    
    amp_hour_rating              = battery.cell.nominal_capacity  # 
    nominal_voltage              = battery.cell.nominal_voltage       
    total_battery_assemply_mass  = battery.cell.mass * battery.module_config.series * battery.module_config.parallel  
    
    battery.mass_properties.mass = total_battery_assemply_mass*module_weight_factor  
    battery.specific_energy      = (amp_hour_rating*nominal_voltage)/battery.cell.mass  * Units.Wh/Units.kg   
    battery.max_energy           = total_battery_assemply_mass*battery.specific_energy    
    battery.max_voltage          = battery.cell.max_voltage  * battery.module_config.series   
    battery.initial_max_energy   = battery.max_energy    
    
    battery.charging_voltage     = battery.cell.charging_voltage * battery.module_config.series     
    battery.charging_current     = battery.cell.charging_current * battery.module_config.parallel    