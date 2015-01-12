# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes.
Email: danaukes<at>seas.harvard.edu.
Please see LICENSE.txt for full license.
"""

import popupcad
from popupcad.manufacturing.multivalueoperation2 import MultiValueOperation2
from popupcad.filetypes.operation import Operation
from .. import algorithms
from .outersheet3 import OuterSheet3

class OuterSheet2(MultiValueOperation2):
    name = 'Sheet'
    show = []
    valuenames = ['Buffer']
    defaults = [0.]
    upgradeclass = OuterSheet3

    def operate(self,design):
        from ..algorithms import web
        ls1 = design.op_from_ref(self.operation_link1).output[self.getoutputref()].csg
        ls,dummy = web.supportsheet(design.return_layer_definition(),ls1,self.values[0]*popupcad.internal_argument_scaling)
        return ls
                
