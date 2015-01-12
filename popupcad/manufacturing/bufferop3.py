# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes.
Email: danaukes<at>seas.harvard.edu.
Please see LICENSE.txt for full license.
"""

import popupcad
from .multivalueoperation3 import MultiValueOperation3
from popupcad.filetypes.operation import Operation

class BufferOperation3(MultiValueOperation3):
    name = 'Buffer'
    show = []
#    function = 'buffer'
    valuenames = ['Buffer','Resolution']
    defaults = [0.,popupcad.default_buffer_resolution]

    def operate(self,design):
        link,output = self.operation_links['parent'][0]
        ls1 = design.op_from_ref(link).output[output].csg
        return ls1.buffer(self.values[0]*popupcad.internal_argument_scaling,resolution = int(self.values[1]))