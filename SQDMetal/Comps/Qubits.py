# -*- coding: utf-8 -*-
# This code is part of Qiskit.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of`` this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# -*- coding: utf-8 -*-
# Author: Divita Gautam
# Creation Date: 21/05/2024
# Description: Collection of classes to draw modified transmon qubits.
"""Transmon Pocket Teeth.
"""

import numpy as np
from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import BaseQubit
from shapely.geometry.base import CAP_STYLE
from shapely.geometry import Polygon
from SQDMetal.Utilities.QUtilities import QUtilities 
from shapely.geometry import LineString

class TransmonTaperred(BaseQubit):
    """Transmon pocket with 'Teeth' connection pads.

    Inherits `BaseQubit` class

    Description:
        Create a standard pocket transmon qubit for a ground plane with teeth
        Here we use the 'Teeth' shape which ones connected to the top pad and one connection pad.

    Options:
        Convention: Values (unless noted) are strings with units included,
        (e.g., '30um')

    Pocket:
        * pad_gap            - the distance between the two charge islands, which is also the
          resulting 'length' of the pseudo junction
        * inductor_width     - width of the pseudo junction between the two charge islands (should be same as josephson junction width)
        * inductor_height    - height of the pseudo junction between the two charge islands 
        * pad_width          - the width (x-axis) of the charge island pads, except the circle radius from both sides
        * pad_height         - the size (y-axis) of the charge island pads
        * fillet_resolution_pad - number of points used to calculate the fillet/curve for the qubit pads
        * pocket_width       - size of the pocket (cut out in ground) along x-axis
        * pocket_height      - size of the pocket (cut out in ground) along y-axis
        * fillet_radius_gap  - The radius of the curved edges of the pocket
        * fillet_resolution_gap  - number of points used to calculate the fillet/curve for the gap
        * chrgln_pin_x_offset =     - horizontal distance of the pin from the qubit center
        * chrgln_pin_y_offset =     - vertical distance of the pin from the pocket edge
        * coupled_pad_gap    - the distance between the two teeth shape
        * coupled_pad_width  - the width (x-axis) of the teeth shape on the island pads
        * coupled_pad_height - the size (y-axis) of the teeth shape on the island pads
        * taper_width_top    - top width of tapered bandage
        * taper_width_base   - bottom width of tapered bandage
        * taper_height      -  height of tapered bandage
        * fillet_radius_tapered - fillet radius to curve edges   
        * fillet_resolution_tapered - number of points used to calculate the fillet/curve
        * ignore_slope_check - To ignore the slope check which should be less than 0.4
        * coupled_pad_height - height of the qubit teeth
        * coupled_pad_width  - width of qubit teeth 
        * coupled_pad_gap='50um',  # One can arrange the gap between the teeth.
        * fillet_radius_teeth= '2um',
        * fillet_resolution_teeth_curve=4,   # to control the curvature of the teeth
        * fillet_resolution_teeth_joint =4,                  

    Connector lines:
        * pad_gap        - space between the connector pad and the charge island it is
          nearest to
        * pad_width      - width (x-axis) of the connector pad
        * pad_height     - height (y-axis) of the connector pad
        * pad_cpw_shift  - shift the connector pad cpw line by this much away from qubit
        * pad_cpw_extent - how long should the pad be - edge that is parallel to pocket
        * cpw_width      - center trace width of the CPW line
        * cpw_gap        - dielectric gap width of the CPW line
        * cpw_extend     - depth the connector line extends into ground (past the pocket edge)
        * pocket_extent  - How deep into the pocket should we penetrate with the cpw connector
        * fillet_radius - The radius of the curved edges of the connector pad
          (into the ground plane)
        * pocket_rise    - How far up or down relative to the center of the transmon should we
          elevate the cpw connection point on the ground plane
        * loc_W / H      - which 'quadrant' of the pocket the connector is set to, +/- 1 (check
          if diagram is correct)


    Sketch:
        Below is a sketch of the qubit
        ::

                 +1              0             +1
                _________________________________
            -1  |                |               |  +1      Y
                |           | | |_| | |          |          ^
                |        ___| |_____| |____      |          |
                |       /     island       \     |          |----->  X
                |       \__________________/     |
                |             |       |          |
                |               |   |            |
                |                |_|             |
                |                |               |
                |                |               |
                |  pocket        x               |                                              
                |                |               |  
                |                ||              |    
                |               |  |             |                      
                |        _____|______|_____      |
                |       /                  \     |
                |       \__________________/     |
                |                                |
                |                                |
            -1  |________________________________|                          
                            

    .. meta::
        Transmon Pocket Teeth

    """

    #_img = 'transmon_pocket1.png'

    # Default drawing options
    default_options = Dict(
        pad_gap='100um',
        inductor_width='30um',
        inductor_height='5um',
        pad_width='400um',
        pad_height='90um',
        fillet_resolution_pad = 16,
        pocket_width='650um',
        pocket_height='650um',
        fillet_radius_gap='30um',
        fillet_resolution_gap=4,
        chrgln_pin_x_offset = '30um',  # User-defined horizontal distance from the qubit center
        chrgln_pin_y_offset = '50um', # User-defined vertical distance from the pocket edge
        #Taperred part of qubit
        taper_width_top='100um',
        taper_width_base='150um',
        taper_height='30um',
        fillet_radius_tapered='1um',    
        fillet_resolution_tapered=4, #this is being used to curve the teeth joininh as well 
        ignore_slope_check=False,
        # coupled_pad belongs to the teeth part. Teeth will have same height/width and are symmetric.
        coupled_pad_height='150um',
        coupled_pad_width='20um',
        coupled_pad_gap='50um',  # One can arrange the gap between the teeth.
        fillet_radius_teeth= '2um',
        fillet_resolution_teeth_curve=4,   # to control the curvature of the teeth
        fillet_resolution_teeth_joint =4,
        # orientation = 90 has dipole aligned along the +X axis, while 0 aligns to the +Y axis
        _default_connection_pads=Dict(
            pad_gap='15um',
            pad_width='20um',
            pad_height='150um',
            pad_cpw_shift='0um',
            pad_cpw_extent='25um',
            cpw_width='10um',
            cpw_gap='6um',
            # edge_curve=0.1,
            # : cpw_extend: how far into the ground to extend the CPW line from the coupling pads
            cpw_extend='100um',
            pocket_extent='5um',
            pocket_rise='0um',
            fillet_radius='1um',
            fillet_resolution=4,
            loc_W='+1',  # width location  only +-1 or 0,
            loc_H='+1',  # height location  only +-1 or 0
        ))
    # """Default drawing options"""

    component_metadata = Dict(short_name='Pocket',
                              _qgeometry_table_path='True',
                              _qgeometry_table_poly='True',
                              _qgeometry_table_junction='True')
    # """Component metadata"""

    # TOOLTIP = """Transmon pocket with teeth pads."""

    # def make(self):
    def __init__(self, design,
                    name: str = None,
                    options: Dict = None,
                    **kwargs):
        super().__init__(design, name, options, **kwargs)
        
        if not options.get('ignore_slope_check'):
        # Compute and validate slope
            taper_width_top = float(options.get('taper_width_top', '100um')[:-2])
            taper_width_base = float(options.get('taper_width_base', '150um')[:-2])
            taper_height = float(options.get('taper_height', '30um')[:-2])

            computed_slope = (2 * taper_height) / (taper_width_base - taper_width_top)
            assert computed_slope < 0.4, f"Slope {computed_slope:.2f} is too steep! Adjust taper dimensions for the slope to be less than 0.4."
    
    def make(self):   
        self.make_pocket()
        self.make_connection_pads()

    #Function to create trapered trapezoid
    def create_trapezoid(self, center_x, top_width, base_width, height, y_offset, rfillet, startx):
        half_top = float(top_width) / 2
        half_base = float(base_width) / 2
        coordinates = [
            (center_x - half_base, y_offset),
            (center_x - half_top, y_offset + height),
            (center_x + half_top, y_offset + height),
            (center_x + half_base, y_offset)
        ]
        
        # Create a Polygon object from the coordinates
        trapezoid_polygon = Polygon(coordinates)
        
        # Convert the coordinates to numpy array
        raw_data = np.array(trapezoid_polygon.exterior.coords)

        start_x = center_x - startx
        start_y = y_offset

        end_x = center_x + startx
        end_y = y_offset

        start = [[start_x, start_y]]
        end = [[end_x, end_y]]

        # Concatenate arrays after converting start and end points to 2D arrays
        raw_data_2 = np.vstack((start, raw_data, end))

        raw_data_1=np.delete(raw_data_2,5,0)

        # Curve the edges of the polygon
        data = QUtilities.calc_filleted_path(raw_data_1, rfillet, 9)
        
        # Create a new Polygon object from the curved coordinates
        trapezoid_with_curved_edges = Polygon(data)

        return trapezoid_with_curved_edges
    
        # """Makes standard transmon in a pocket."""

    def make_pocket(self):
            
        # self.p allows us to directly access parsed values (string -> numbers) form the user option
        p = self.p
        #  pcop = self.p.coupled_pads[name]  # parser on connector options

        # since we will reuse these options, parse them once and define them as variables
        pad_width = p.pad_width
        pad_height = p.pad_height
        pad_gap = p.pad_gap
        coupled_pad_height = p.coupled_pad_height
        coupled_pad_width = p.coupled_pad_width
        coupled_pad_gap = p.coupled_pad_gap

        # make the pads as rectangles (shapely polygons)
        pad = draw.rectangle(pad_width, pad_height)

        pad_top = draw.translate(pad, 0, +(pad_height + pad_gap) / 2.)
        # Here, you make your pads round. Not sharp shape on the left and right sides and also this should be the same for the bottom pad as the top pad.
        circ_left_top = draw.Point(-pad_width / 2., +(pad_height + pad_gap) /
                                   2.).buffer(pad_height / 2,
                                              p.fillet_resolution_pad,
                                              cap_style=CAP_STYLE.round)
        circ_right_top = draw.Point(pad_width / 2., +(pad_height + pad_gap) /
                                    2.).buffer(pad_height / 2,
                                               p.fillet_resolution_pad,
                                               cap_style=CAP_STYLE.round)
        # In here you create the teeth part and then you union them as one with the pad. Teeth only belong to top pad.
        coupled_pad = draw.rectangle(coupled_pad_width,
                                     coupled_pad_height + pad_height)
        coupler_pad_round = draw.Point(0., (coupled_pad_height + pad_height) /
                                       2).buffer(coupled_pad_width / 2,
                                                 p.fillet_resolution_teeth_curve,
                                                 cap_style=CAP_STYLE.round)
        coupled_pad = draw.union(coupled_pad, coupler_pad_round)
        coupled_pad_left = draw.translate(
            coupled_pad, -(coupled_pad_width / 2. + coupled_pad_gap / 2.),
            +coupled_pad_height / 2. + pad_height + pad_gap / 2. -
            pad_height / 2)
        coupled_pad_right = draw.translate(
            coupled_pad, (coupled_pad_width / 2. + coupled_pad_gap / 2.),
            +coupled_pad_height / 2. + pad_height + pad_gap / 2. -
            pad_height / 2)
            
        pad_top_tmp1 = draw.union([circ_left_top, pad_top, circ_right_top])

        # Add trapezoid to the top pad
        trapezoid_top = self.create_trapezoid(0, p.taper_width_top, p.taper_width_base, p.taper_height, (pad_gap / 2 )- float(p.taper_height), p.fillet_radius_tapered,p.pad_width/2)
        # pad_top_tmp = draw.union(pad_top_tmp1, trapezoid_top)
        trapezoid_top_rotated = draw.rotate(trapezoid_top, 180, origin=(0,pad_gap/4+(pad_gap/2- float(p.taper_height))/2)) # Rotate trapezoid by 180 degrees
        
        # Apply buffer(0) to fix any invalid geometries
        pad_top_tmp1 = pad_top_tmp1.buffer(0)  # Fix minor topology issues
        trapezoid_top_rotated = trapezoid_top_rotated.buffer(0)
        
        pad_top_tmp = draw.union(pad_top_tmp1, trapezoid_top_rotated)



        # The coupler pads are only created if low_W=0 and low_H=+1
        for name in self.options.connection_pads:
            if self.options.connection_pads[name][
                    'loc_W'] == 0 and self.options.connection_pads[name][
                        'loc_H'] == +1:
                pad_top_tmp = draw.union([
                    circ_left_top, coupled_pad_left, pad_top_tmp, coupled_pad_right,
                    circ_right_top
                ])
        pad_top = pad_top_tmp

        #Curving the edges of the teeth where it joins the pad
        pad_top = pad_top.buffer(p.fillet_radius_teeth, join_style=2, cap_style=3).buffer(-p.fillet_radius_teeth, cap_style=1, join_style=1, mitre_limit=2.0, quad_segs=p.fillet_resolution_teeth_joint)
        pad_top = pad_top.buffer(-p.fillet_radius_teeth, join_style=2, cap_style=3).buffer(p.fillet_radius_teeth, cap_style=1, join_style=1, mitre_limit=2.0, quad_segs=p.fillet_resolution_teeth_joint)

        # Round part for the bottom pad. And again you should unite all of them.
        pad_bot = draw.translate(pad, 0, -(pad_height + pad_gap) / 2.)
        circ_left_bot = draw.Point(-pad_width / 2, -(pad_height + pad_gap) /
                                   2.).buffer(pad_height / 2,
                                              p.fillet_resolution_pad,
                                              cap_style=CAP_STYLE.round)
        circ_right_bot = draw.Point(pad_width / 2, -(pad_height + pad_gap) /
                                    2.).buffer(pad_height / 2,
                                               p.fillet_resolution_pad,
                                               cap_style=CAP_STYLE.round)
        pad_bot = draw.union([pad_bot, circ_left_bot, circ_right_bot])

        # Add trapezoid to the bottom pad
        trapezoid_bot = self.create_trapezoid(0, p.taper_width_top, p.taper_width_base, p.taper_height, -(pad_gap) / 2, p.fillet_radius_tapered,p.pad_width/2)
        pad_bot = draw.union(pad_bot, trapezoid_bot)

###############################################################################################
        # Pins from thr center of the qubit pads 
        #Cordinates for the center of the pin
        taper_width_top = p.taper_width_top 

        top_pin = LineString([
            [0, pad_gap / 2],
            [0, pad_gap / 2 - p.taper_height/2 ]  
              # Extend outward
        ])

        bottom_pin = LineString([
            [0, -pad_gap / 2],
            [0, -pad_gap / 2 + p.taper_height/2 ] # Start from pad bottom edge
              # Extend outward
        ])

###############################################################################################
        ##Pins outside the qubit pocket 
        # Define the pin positions relative to (0,0)
        bottom_pocket_pin = LineString([
            [ p.pocket_width / 2 + p.chrgln_pin_y_offset, p.chrgln_pin_x_offset],
            [ p.pocket_width / 2 + p.chrgln_pin_y_offset,0]  # Start point (near pocket)
             # Extend outward
        ])

        top_pocket_pin = LineString([
            [-p.pocket_width / 2 - p.chrgln_pin_y_offset, p.chrgln_pin_x_offset],
            [-p.pocket_width / 2 - p.chrgln_pin_y_offset,0]  # Start point (near pocket)
              # Extend outward
        ])

###############################################################################################
        # rect_jj = draw.LineString([(0, -pad_gap / 2+p.taper_height), (0, +pad_gap / 2-p.taper_height)])
        
        # the draw.rectangle representing the josephson junction
        rect_jj = draw.rectangle(p.inductor_width, p.inductor_height)
        
        # To make the qubit pocket 
        rect_pk = draw.rectangle(p.pocket_width, p.pocket_height)

        # to curve the edges of the qubit pocket
        rect_pk = rect_pk.buffer(p.fillet_radius_gap, cap_style=1, join_style=1, mitre_limit=2.0, quad_segs=p.fillet_resolution_gap)
        

        # Rotate and translate all qgeometry as needed.
        # Done with utility functions in Metal 'draw_utility' for easy rotation/translation
        # NOTE: Should modify so rotate/translate accepts qgeometry, would allow for
        # smoother implementation.
        polys = [rect_jj, pad_top, pad_bot, rect_pk,top_pin, bottom_pin,top_pocket_pin, bottom_pocket_pin]
        polys = draw.rotate(polys, p.orientation, origin=(0, 0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [rect_jj, pad_top, pad_bot, rect_pk,top_pin, bottom_pin,top_pocket_pin, bottom_pocket_pin] = polys

        # Use the geometry to create Metal qgeometry
        self.add_qgeometry('poly', dict(pad_top=pad_top, pad_bot=pad_bot))
        self.add_qgeometry('poly', dict(rect_pk=rect_pk), subtract=True)
        # self.add_qgeometry('poly', dict(
        #     rect_jj=rect_jj), helper=True)
        self.add_qgeometry('junction',
                           dict(rect_jj=rect_jj),
                           width=p.inductor_width)
        
        #Pins from the center of the qubit pads
        self.add_pin("pin_island", points=list(top_pin.coords), width=taper_width_top, input_as_norm=True)
        self.add_pin("pin_reservior", points=list(bottom_pin.coords), width=taper_width_top, input_as_norm=True)

         # Add pins to the component
        self.add_pin("bottom_pin", points=list(bottom_pocket_pin.coords), width=taper_width_top)
        self.add_pin("top_pin", points=list(top_pocket_pin.coords), width=taper_width_top)

        # print(f"DEBUG: top_pocket_pin coordinates: {list(top_pocket_pin.coords)}")

        ##############################################################################################################
        
        #########################################################################################################################
    def make_connection_pads(self):
        # """Makes standard transmon in a pocket."""
        for name in self.options.connection_pads:
            self.make_connection_pad(name)

    def make_connection_pad(self, name: str):
        # """Makes n individual connector.

        # Args:
        #     name (str) : Name of the connector
        # """

        # self.p allows us to directly access parsed values (string -> numbers) form the user option
        p = self.p
        pc = self.p.connection_pads[name]  # parser on connector options

        # define commonly used variables once
        cpw_width = pc.cpw_width
        cpw_extend = pc.cpw_extend
        pad_width = pc.pad_width
        pad_height = pc.pad_height
        pad_cpw_shift = pc.pad_cpw_shift
        pocket_rise = pc.pocket_rise
        pocket_extent = pc.pocket_extent

        loc_W = float(pc.loc_W)
        loc_W, loc_H = float(pc.loc_W), float(pc.loc_H)
        if float(loc_W) not in [-1., +1., 0] or float(loc_H) not in [-1., +1.]:
            self.logger.info(
                'Warning: Did you mean to define a transmon qubit with loc_W and'
                ' loc_H that are not +1, -1, or 0? Are you sure you want to do this?'
            )

        # Define the geometry
        # Connector pad

        if float(loc_W) != 0:
            connector_pad = draw.rectangle(pad_width, pad_height,
                                           -pad_width / 2, pad_height / 2)
            connector_pad = connector_pad.buffer(pc.fillet_radius, cap_style=1, join_style=1, mitre_limit=2.0, quad_segs=pc.fillet_resolution) 
            # Connector CPW wire
            connector_wire_path = draw.wkt.loads(f"""LINESTRING (\
                0 {pad_cpw_shift+cpw_width/2}, \
                {pc.pad_cpw_extent}                           {pad_cpw_shift+cpw_width/2}, \
                {(p.pocket_width-p.pad_width)/2-pocket_extent} {pad_cpw_shift+cpw_width/2+pocket_rise}, \
                {(p.pocket_width-p.pad_width)/2+cpw_extend}    {pad_cpw_shift+cpw_width/2+pocket_rise}\
                                            )""")
        else:
            connector_pad = draw.rectangle(pad_width, pad_height, 0,
                                           pad_height / 2)
            connector_pad = connector_pad.buffer(pc.fillet_radius, cap_style=1, join_style=1, mitre_limit=2.0, quad_segs=pc.fillet_resolution)
            
        ## Made chnages here to add buffer to curve edges 
            # connector_pad=connector_pad_1.buffer(p.edge_curve)
            connector_wire_path = draw.LineString(
                [[0, pad_height],
                 [
                     0,
                     (p.pocket_width / 2 - p.pad_height - p.pad_gap / 2 -
                      pc.pad_gap) + cpw_extend
                 ]])

        # Position the connector, rotate and translate
        objects = [connector_pad, connector_wire_path]

        if loc_W == 0:
            loc_Woff = 1
        else:
            loc_Woff = loc_W

        objects = draw.scale(objects, loc_Woff, loc_H, origin=(0, 0))
        objects = draw.translate(
            objects,
            loc_W * (p.pad_width) / 2.,
            loc_H * (p.pad_height + p.pad_gap / 2 + pc.pad_gap))
        objects = draw.rotate_position(objects, p.orientation,
                                       [p.pos_x, p.pos_y])
        [connector_pad, connector_wire_path] = objects

        self.add_qgeometry('poly', {f'{name}_connector_pad': connector_pad})
        self.add_qgeometry('path', {f'{name}_wire': connector_wire_path},
                           width=cpw_width)
        self.add_qgeometry('path', {f'{name}_wire_sub': connector_wire_path},
                           width=cpw_width + 2 * pc.cpw_gap,
                           subtract=True)

        ############################################################

        # add pins
        points = np.array(connector_wire_path.coords)
        self.add_pin(name,
                     points=points[-2:],
                     width=cpw_width,
                     input_as_norm=True)

        
###################################################################################################################################
