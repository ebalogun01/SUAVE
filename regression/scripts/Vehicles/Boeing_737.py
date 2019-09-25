# Boeing_737.py
#
# Created:  Feb 2017, M. Vegh (taken from data originally in B737/mission_B737.py, noise_optimization/Vehicles.py, and Boeing 737 tutorial script
# Modified: Jul 2017, M. Clarke

""" setup file for the Boeing 737 vehicle
"""
# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
import numpy as np
import SUAVE
from SUAVE.Core import Units
from SUAVE.Methods.Propulsion.turbofan_sizing import turbofan_sizing
from SUAVE.Methods.Geometry.Two_Dimensional.Cross_Section.Propulsion.compute_turbofan_geometry import compute_turbofan_geometry 
# ----------------------------------------------------------------------
#   Define the Vehicle
# ----------------------------------------------------------------------
def vehicle_setup():
    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------   
    vehicle                                           = SUAVE.Vehicle()
    vehicle.tag                                       = 'Boeing_737800'    
   
    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------    
    # mass properties
    vehicle.mass_properties.max_takeoff               = 79015.8   # kg
    vehicle.mass_properties.takeoff                   = 79015.8   # kg
    vehicle.mass_properties.operating_empty           = 62746.4   # kg
    vehicle.mass_properties.takeoff                   = 79015.8   # kg
    vehicle.mass_properties.max_zero_fuel             = 62732.0   # kg #0.9 * vehicle.mass_properties.max_takeoff
    vehicle.mass_properties.cargo                     = 10000.  * Units.kilogram   
    vehicle.mass_properties.center_of_gravity         = [ 15.30987849,   0.        ,  -0.48023939]
    vehicle.mass_properties.moments_of_inertia        = [[3173074.17, 0 , 28752.77565],[0 , 3019041.443, 0],[0, 0, 5730017.433]] # estimated, not correct 
    
    # envelope properties
    vehicle.envelope.ultimate_load        = 2.5
    vehicle.envelope.limit_load           = 1.5
                                          
    # basic parameters                    
    vehicle.reference_area                = 124.862       
    vehicle.passengers                    = 170
    vehicle.systems.control               = "fully powered" 
    vehicle.systems.accessories           = "medium range"


    # ------------------------------------------------------------------        
    #   Main Wing
    # ------------------------------------------------------------------        
    wing                                  = SUAVE.Components.Wings.Main_Wing()
    wing.tag                              = 'main_wing'
    wing.aspect_ratio                     = 10.18 # Not set
    wing.thickness_to_chord               = 0.1 # Not set
    wing.taper                            = 0.782/7.7760
    wing.span_efficiency                  = 0.9 
    wing.spans.projected                  = 34.32    
    wing.chords.root                      = 7.760 * Units.meter
    wing.chords.tip                       = 0.782 * Units.meter
    wing.chords.mean_aerodynamic          = 4.235 * Units.meter
    wing.areas.reference                  = 124.862  # Not set
    wing.sweeps.quarter_chord             = 25. * Units.degrees
    wing.twists.root                      = 4.0 * Units.degrees
    wing.twists.tip                       = 0.0 * Units.degrees
    wing.dihedral                         = 2.5 * Units.degrees
    wing.origin                           = [13.61,0,-1.27]
    wing.aerodynamic_center               = [0,0,0] 
    wing.vertical                         = False
    wing.symmetric                        = True
    wing.high_lift                        = True
    wing.dynamic_pressure_ratio           = 1.0 
                                          
    # Wing Segments                       
    root_airfoil                          = SUAVE.Components.Wings.Airfoils.Airfoil()
    root_airfoil.coordinate_file          = 'B737a.txt'   
    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'Root'
    segment.percent_span_location         = 0.0
    segment.twist                         = 4. * Units.deg
    segment.root_chord_percent            = 1.
    segment.dihedral_outboard             = 2.5 * Units.degrees
    segment.sweeps.quarter_chord          = 28.225 * Units.degrees
    segment.append_airfoil(root_airfoil)
    wing.append_segment(segment)    
    
    yehudi_airfoil                        = SUAVE.Components.Wings.Airfoils.Airfoil()
    yehudi_airfoil.coordinate_file        = 'B737b.txt'   
    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'Yehudi'
    segment.percent_span_location         = 0.324
    segment.twist                         = (wing.twists.root*(1-segment.percent_span_location)) * Units.deg
    segment.root_chord_percent            = 0.5
    segment.dihedral_outboard             = 5.5 * Units.degrees
    segment.sweeps.quarter_chord          = 25. * Units.degrees
    segment.append_airfoil(yehudi_airfoil)
    wing.append_segment(segment)

    mid_airfoil                           = SUAVE.Components.Wings.Airfoils.Airfoil()
    mid_airfoil.coordinate_file           = 'B737c.txt' 
    segment                               = SUAVE.Components.Wings.Segment()
    segment.tag                           = 'Section_2'
    segment.percent_span_location         = 0.963
    segment.twist                         = (wing.twists.root*(1-segment.percent_span_location)) * Units.deg
    segment.root_chord_percent            = 0.220
    segment.dihedral_outboard             = 5.5 * Units.degrees
    segment.sweeps.quarter_chord          = 56.75 * Units.degrees
    segment.append_airfoil(mid_airfoil)
    wing.append_segment(segment)
    
    tip_airfoil                           =  SUAVE.Components.Wings.Airfoils.Airfoil()
    tip_airfoil.coordinate_file           = 'B737c.txt' 
    segment                               = SUAVE.Components.Wings.Segment() 
    segment.tag                           = 'Tip'
    segment.percent_span_location         = 1.
    segment.twist                         = 0. * Units.degrees
    segment.root_chord_percent            = 0.10077
    segment.dihedral_outboard             = 0.
    segment.sweeps.quarter_chord          = 0.
    segment.append_airfoil(tip_airfoil)
    wing.append_segment(segment)     
       
    # control surfaces -------------------------------------------
    control_surface                       = SUAVE.Components.Wings.Control_Surface() 
    control_surface.tag                   = 'flap'
    control_surface.function              = 'flap' 
    control_surface.span_fraction_start   = 0.10 
    control_surface.span_fraction_end     = 0.75   
    control_surface.deflection            = 1.0 * Units.degrees
    control_surface.configuration_type    = 'double_slotted'
    control_surface.chord_fraction        = 0.30   
    wing.append_control_surface(control_surface)    
    
    #wing.flaps.chord      =  0.30   
    #wing.flaps.span_start =  0.10   # ->     wing.flaps.area = 97.1112
    #wing.flaps.span_end   =  0.75
    #wing.flaps.type       = 'double_slotted'  # -> wing.flaps.number_slots = 2
        
    control_surface                       = SUAVE.Components.Wings.Control_Surface() 
    control_surface.tag                   = 'slat'
    control_surface.function              = 'slat' 
    control_surface.span_fraction_start   = 0.324 
    control_surface.span_fraction_end     = 0.963     
    control_surface.deflection            = 1.0 * Units.degrees
    control_surface.chord_fraction        = 0.1  	 
    wing.append_control_surface(control_surface)  
        
    control_surface                       = SUAVE.Components.Wings.Control_Surface() 
    control_surface.tag                   = 'aileron'
    control_surface.function              = 'aileron'
    control_surface.span_fraction_start   = 0.7 
    control_surface.span_fraction_end     = 0.963 
    control_surface.deflection            = 1.0 * Units.degrees
    control_surface.chord_fraction        = 0.16    
    wing.append_control_surface(control_surface)         
    
    # add to vehicle
    vehicle.append_component(wing)
    
    # ------------------------------------------------------------------        
    #  Horizontal Stabilizer
    # ------------------------------------------------------------------      
    wing                                  = SUAVE.Components.Wings.Wing()
    wing.tag                              = 'horizontal_stabilizer'
    wing.aspect_ratio                     = 5.023 
    wing.thickness_to_chord               = 0.08 
    wing.taper                            = 0.203
    wing.span_efficiency                  = 0.9
    wing.spans.projected                  = 14.2
    wing.chords.root                      = 4.70
    wing.chords.tip                       = 0.9541   
    wing.chords.mean_aerodynamic          = 3.241  
    wing.areas.reference                  = 40.14 
    wing.areas.exposed                    = 59.354                   # Exposed area of the horizontal tail
    wing.areas.wetted                     = 64.976                   # Wetted area of the horizontal tail    
    wing.twists.root                      = 0.0 * Units.degrees
    wing.twists.tip                       = 0.0 * Units.degrees 
    wing.sweeps.quarter_chord             = 38.42 * Units.degrees
    wing.origin                           = [32.83,0,1.14]
    wing.aerodynamic_center               = [0,0,0]
    wing.dihedral                         = 8.63 * Units.degrees
    wing.vertical                         = False 
    wing.symmetric                        = True
    wing.dynamic_pressure_ratio           = 0.9  
                                          
    # Wing Segments                       
    segment                               = SUAVE.Components.Wings.Segment() 
    segment.tag                           = 'root_segment'
    segment.percent_span_location         = 0.0
    segment.twist                         = 0. * Units.deg
    segment.root_chord_percent            = 1.0
    segment.dihedral_outboard             = 8.63 * Units.degrees
    segment.sweeps.quarter_chord          = 38.42 * Units.degrees
    wing.append_segment(segment)                 
                                          
    segment                               = SUAVE.Components.Wings.Segment() 
    segment.tag                           = 'tip_segment'
    segment.percent_span_location         = 1.
    segment.twist                         = 0. * Units.deg
    segment.root_chord_percent            = 0.203
    segment.dihedral_outboard             = 0 * Units.degrees
    segment.sweeps.quarter_chord          = 0 * Units.degrees
    wing.append_segment(segment) 
    
    # control surfaces -------------------------------------------
    control_surface                       = SUAVE.Components.Wings.Control_Surface() 
    control_surface.tag                   = 'elevator'
    control_surface.function              = 'elevator'
    control_surface.span_fraction_start   = 0.09 
    control_surface.span_fraction_end     = 0.92
    control_surface.deflection            = 1.0  * Units.deg
    control_surface.chord_fraction        = 0.3   
    wing.append_control_surface(control_surface)  

    # add to vehicle
    vehicle.append_component(wing)


    # ------------------------------------------------------------------
    #   Vertical Stabilizer
    # ------------------------------------------------------------------
    wing                                  = SUAVE.Components.Wings.Wing()
    wing.tag                              = 'vertical_stabilizer'    
    wing.aspect_ratio                     = 1.91
    wing.sweep                            = 25. * Units.deg
    wing.thickness_to_chord               = 0.08
    wing.taper                            = 0.25
    wing.span_efficiency                  = 0.9
    wing.spans.projected                  = 7.77
    wing.chords.root                      = 8.19
    wing.chords.tip                       = 0.95
    wing.chords.mean_aerodynamic          = 4.0
    wing.areas.reference                  = 27.316
    wing.twists.root                      = 0.0 * Units.degrees
    wing.twists.tip                       = 0.0 * Units.degrees  
    wing.origin                           = [28.79,0,1.54]
    wing.aerodynamic_center               = [0,0,0]    
    wing.vertical                         = True 
    wing.symmetric                        = False
    wing.t_tail                           = False
    wing.dynamic_pressure_ratio           = 1.0
                                          
    # Wing Segments                       
    segment                               = SUAVE.Components.Wings.Segment() 
    segment.tag                           = 'root'
    segment.percent_span_location         = 0.0
    segment.twist                         = 0. * Units.deg
    segment.root_chord_percent            = 1.
    segment.dihedral_outboard             = 0 * Units.degrees
    segment.sweeps.quarter_chord          = 63.63 * Units.degrees
    wing.append_segment(segment)              
                                          
    segment                               = SUAVE.Components.Wings.Segment() 
    segment.tag                           = 'segment_1'
    segment.percent_span_location         = 0.194
    segment.twist                         = 0. * Units.deg
    segment.root_chord_percent            = 0.540
    segment.dihedral_outboard             = 0. * Units.degrees
    segment.sweeps.quarter_chord          = 30.0 * Units.degrees
    wing.append_segment(segment)          
                                          
    segment                               = SUAVE.Components.Wings.Segment() 
    segment.tag                           = 'segment_2'
    segment.percent_span_location         = 0.961
    segment.twist                         = 0. * Units.deg
    segment.root_chord_percent            = 0.175
    segment.dihedral_outboard             = 0.0 * Units.degrees
    segment.sweeps.quarter_chord          = 51.0 * Units.degrees
    wing.append_segment(segment)        
    
    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------
    #  Fuselage
    # ------------------------------------------------------------------
    fuselage                                    = SUAVE.Components.Fuselages.Fuselage()
    fuselage.tag                                = 'fuselage'  
    fuselage.number_coach_seats                 = vehicle.passengers
    fuselage.seats_abreast                      = 6
    fuselage.seat_pitch                         = 1
    fuselage.fineness.nose                      = 1.57
    fuselage.fineness.tail                      = 3.2
    fuselage.lengths.nose                       = 8.0
    fuselage.lengths.tail                       = 12.
    fuselage.lengths.cabin                      = 28.85
    fuselage.lengths.total                      = 38.02
    fuselage.lengths.fore_space                 = 6.
    fuselage.lengths.aft_space                  = 5.    
    fuselage.width                              = 3.7
    fuselage.heights.maximum                    = 3.76
    fuselage.heights.at_quarter_length          = 3.76
    fuselage.heights.at_three_quarters_length   = 3.65
    fuselage.heights.at_wing_root_quarter_chord = 3.76
    fuselage.areas.side_projected               = 142.1948
    fuselage.areas.wetted                       = 446.718
    fuselage.areas.front_projected              = 12.57                                       
    fuselage.effective_diameter                 = 3.76
    fuselage.differential_pressure              = 5.0e4 * Units.pascal #
    
    # add to vehicle
    vehicle.append_component(fuselage)


    # ------------------------------------------------------------------
    #   Turbofan Network
    # ------------------------------------------------------------------    
    turbofan                             =  SUAVE.Components.Energy.Networks.Turbofan()
    turbofan.tag                         =  'turbofan'
    turbofan.number_of_engines           =  2.0
    turbofan.bypass_ratio                =  5.4
    turbofan.engine_length               =  4.1
    turbofan.nacelle_diameter            =  0.85
    turbofan.origin                      =  [[13.72, 4.86,-1.9],[13.72, -4.86,-1.9]]
    turbofan.working_fluid               =  SUAVE.Attributes.Gases.Air()

    #  Component 1 - Ram
    ram                                  = SUAVE.Components.Energy.Converters.Ram()
    ram.tag                              = 'ram'
    turbofan.append(ram)

    #  Component 2 - Inlet Nozzle
    inlet_nozzle                         = SUAVE.Components.Energy.Converters.Compression_Nozzle()
    inlet_nozzle.tag                     = 'inlet_nozzle'
    inlet_nozzle.polytropic_efficiency   = 0.98
    inlet_nozzle.pressure_ratio          = 0.98
    turbofan.append(inlet_nozzle)       


    #  Component 3 - Low Pressure Compressor
    compressor                           = SUAVE.Components.Energy.Converters.Compressor()    
    compressor.tag                       = 'low_pressure_compressor'
    compressor.polytropic_efficiency     = 0.91
    compressor.pressure_ratio            = 1.14    
    turbofan.append(compressor)          

    #  Component 4 - High Pressure Compressor
    compressor                           = SUAVE.Components.Energy.Converters.Compressor()    
    compressor.tag                       = 'high_pressure_compressor'
    compressor.polytropic_efficiency     = 0.91
    compressor.pressure_ratio            = 13.415    
    turbofan.append(compressor)         

    #  Component 5 - Low Pressure Turbine
    turbine                             = SUAVE.Components.Energy.Converters.Turbine()   
    turbine.tag                         ='low_pressure_turbine'
    turbine.mechanical_efficiency       = 0.99
    turbine.polytropic_efficiency       = 0.93     
    turbofan.append(turbine)

    #  Component 6 - High Pressure Turbine
    turbine                             = SUAVE.Components.Energy.Converters.Turbine()   
    turbine.tag                         ='high_pressure_turbine'
    turbine.mechanical_efficiency       = 0.99
    turbine.polytropic_efficiency       = 0.93     
    turbofan.append(turbine)

    #  Component 7 - Combustor
    combustor                           = SUAVE.Components.Energy.Converters.Combustor()   
    combustor.tag                       = 'combustor'
    combustor.efficiency                = 0.99 
    combustor.alphac                    = 1.0     
    combustor.turbine_inlet_temperature = 1450
    combustor.pressure_ratio            = 0.95
    combustor.fuel_data                 = SUAVE.Attributes.Propellants.Jet_A()  
    turbofan.append(combustor)

    #  Component 8 - Core Nozzle
    nozzle                              = SUAVE.Components.Energy.Converters.Expansion_Nozzle()   
    nozzle.tag                          = 'core_nozzle'
    nozzle.polytropic_efficiency        = 0.95
    nozzle.pressure_ratio               = 0.99    
    turbofan.append(nozzle)

    #  Component 9 - Fan Nozzle
    nozzle                              = SUAVE.Components.Energy.Converters.Expansion_Nozzle()   
    nozzle.tag                          = 'fan_nozzle'
    nozzle.polytropic_efficiency        = 0.95
    nozzle.pressure_ratio               = 0.99    
    turbofan.append(nozzle)

    #  Component 10 - Fan
    fan                                 = SUAVE.Components.Energy.Converters.Fan()   
    fan.tag                             = 'fan'
    fan.polytropic_efficiency           = 0.93
    fan.pressure_ratio                  = 1.7    
    turbofan.append(fan)

    # Component 10 : thrust (to compute the thrust)
    thrust                              = SUAVE.Components.Energy.Processes.Thrust()       
    thrust.tag                          ='compute_thrust'
    #total design thrust (includes all the engines)
    thrust.total_design                 = 2*24000. * Units.N #Newtons

    #design sizing conditions
    altitude                            = 35000.0*Units.ft
    mach_number                         = 0.78 
    isa_deviation                       = 0.

    # add to network
    turbofan.thrust                     = thrust
    turbofan.core_nozzle_diameter       = 0.92
    turbofan.fan_nozzle_diameter        = 1.659
    turbofan.engine_height              = 0.5  #Engine centerline heigh above the ground plane
    turbofan.exa                        = 1    #distance from fan face to fan exit/ fan diameter)
    turbofan.plug_diameter              = 0.1  #dimater of the engine plug 
    turbofan.geometry_xe                = 1. # Geometry information for the installation effects function
    turbofan.geometry_ye                = 1. # Geometry information for the installation effects function   
    turbofan.geometry_Ce                = 2. # Geometry information for the installation effects function
    
    #size the turbofan
    turbofan_sizing(turbofan,mach_number,altitude)   

    #computing the engine length and diameter
    compute_turbofan_geometry(turbofan,None) 

    # add  gas turbine network gt_engine to the vehicle 
    vehicle.append_component(turbofan)      
    
    # ------------------------------------------------------------------        
    #  Fuel
    # ------------------------------------------------------------------        
    fuel                                  = SUAVE.Components.Physical_Component()
    vehicle.fuel                          = fuel
    fuel.mass_properties.mass             = vehicle.mass_properties.max_takeoff-vehicle.mass_properties.max_fuel
    fuel.origin                           = vehicle.wings.main_wing.mass_properties.center_of_gravity     
    fuel.mass_properties.center_of_gravity= vehicle.wings.main_wing.aerodynamic_center

    # ------------------------------------------------------------------        
    #  Landing Gear
    # ------------------------------------------------------------------        
    landing_gear                          = SUAVE.Components.Landing_Gear.Landing_Gear()
    landing_gear.tag                      = "main_landing_gear"
    landing_gear.main_tire_diameter       = 1.12000 * Units.m
    landing_gear.nose_tire_diameter       = 0.6858 * Units.m
    landing_gear.main_strut_length        = 1.8 * Units.m
    landing_gear.nose_strut_length        = 1.3 * Units.m
    landing_gear.main_units               = 1      #number of nose landing gear
    landing_gear.nose_units               = 1     #number of nose landing gear
    landing_gear.main_wheels              = 2    #number of wheels on the main landing gear
    landing_gear.nose_wheels              = 2    #number of wheels on the nose landing gear      
    vehicle.landing_gear                  = landing_gear
    
    # ------------------------------------------------------------------
    #   Vehicle Definition Complete
    # ------------------------------------------------------------------

    return vehicle


# ----------------------------------------------------------------------
#   Define the Configurations
# ---------------------------------------------------------------------

def configs_setup(vehicle):
    
    # ------------------------------------------------------------------
    #   Initialize Configurations
    # ------------------------------------------------------------------
    configs = SUAVE.Components.Configs.Config.Container()
    base_config = SUAVE.Components.Configs.Config(vehicle)
    base_config.tag = 'base'
    configs.append(base_config)

    # ------------------------------------------------------------------
    #   Cruise Configuration
    # ------------------------------------------------------------------
    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'cruise'
    configs.append(config)

    # ------------------------------------------------------------------
    #   Takeoff Configuration
    # ------------------------------------------------------------------
    config = SUAVE.Components.Configs.Config(base_config)
    config.tag                                                       = 'takeoff'
    config.wings['main_wing'].control_surfaces.flap.deflection       = 20. * Units.deg
    config.wings['main_wing'].control_surfaces.slat.deflection       = 25. * Units.deg
    config.max_lift_coefficient_factor                               = 1. #0.95
    #Noise input for the landing gear                                
    config.landing_gear.gear_condition                               = 'up'       
    config.output_filename                                           = 'Flyover_' 
    config.propulsors['turbofan'].fan.rotation                       = 3470. #N1 speed
    config.propulsors['turbofan'].fan_nozzle.noise_speed             = 315.
    config.propulsors['turbofan'].core_nozzle.noise_speed            = 415.

    configs.append(config)
    
    # ------------------------------------------------------------------
    #   Cutback Configuration
    # ------------------------------------------------------------------
    config = SUAVE.Components.Configs.Config(base_config)
    config.tag                                                       = 'cutback'
    config.wings['main_wing'].control_surfaces.flap.deflection       = 20. * Units.deg
    config.wings['main_wing'].control_surfaces.slat.deflection       = 20. * Units.deg
    config.max_lift_coefficient_factor                               = 1. #0.95
    #Noise input for the landing gear                                
    config.landing_gear.gear_condition                               = 'up'       
    config.output_filename                                           = 'Cutback_'  
    config.propulsors['turbofan'].fan.rotation                       = 2780. #N1 speed
    config.propulsors['turbofan'].fan_nozzle.noise_speed             = 210.
    config.propulsors['turbofan'].core_nozzle.noise_speed            = 360.
    config.V2_VS_ratio                                               = 1.21
    config.maximum_lift_coefficient                                  = 2.
    configs.append(config)    

    # ------------------------------------------------------------------
    #   Landing Configuration
    # ------------------------------------------------------------------

    config = SUAVE.Components.Configs.Config(base_config)
    config.tag                                                       = 'landing' 
    config.wings['main_wing'].control_surfaces.flap.deflection       = 30. * Units.deg
    config.wings['main_wing'].control_surfaces.slat.deflection       = 25. * Units.deg  
    config.max_lift_coefficient_factor                               = 1. #0.95
    #Noise input for the landing gear                              
    config.landing_gear.gear_condition                               = 'down'    
    config.output_filename                                           = 'Approach_' 
    config.propulsors['turbofan'].fan.rotation                       = 2030.  #N1 speed
    config.propulsors['turbofan'].fan_nozzle.noise_speed             = 109.3
    config.propulsors['turbofan'].core_nozzle.noise_speed            = 92.
    config.Vref_VS_ratio                                             = 1.23
    config.maximum_lift_coefficient                                  = 2.

    configs.append(config)

    # ------------------------------------------------------------------
    #   Short Field Takeoff Configuration
    # ------------------------------------------------------------------  
    config = SUAVE.Components.Configs.Config(base_config)
    config.tag                                                       = 'short_field_takeoff' 
    config.wings['main_wing'].control_surfaces.flap.deflection       = 20. * Units.deg
    config.wings['main_wing'].control_surfaces.slat.deflection       = 20. * Units.deg
    config.V2_VS_ratio                                               = 1.21
    config.max_lift_coefficient_factor                               = 2. #0.95
  
    configs.append(config)

    return configs