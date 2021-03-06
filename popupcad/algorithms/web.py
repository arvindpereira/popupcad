# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

from popupcad.filetypes.genericshapes import GenericPoly
from popupcad.filetypes.laminate import Laminate
import numpy
import popupcad

def supportsheet(layerdef, lsin, value):
    allext = []
    for layer, layer_geometry in lsin.layer_sequence.items():
        for geom in layer_geometry.geoms:
            geom2 = popupcad.algorithms.csg_shapely.to_generic(geom)
            allext.extend(geom2.exteriorpoints(scaling = popupcad.csg_processing_scaling))
    allext = numpy.array(allext)
    minx = allext[:, 0].min() - value
    miny = allext[:, 1].min() - value
    maxx = allext[:, 0].max() + value
    maxy = allext[:, 1].max() + value
    exterior = [[minx, miny], [maxx, miny], [maxx, maxy], [minx, maxy]]
    exterior_scaled = (numpy.array(exterior)/popupcad.csg_processing_scaling).tolist()
    geom = GenericPoly.gen_from_point_lists(exterior_scaled, [])
    geom = geom.to_shapely(scaling = popupcad.csg_processing_scaling)
    ls = Laminate(layerdef)
    [ls.replacelayergeoms(layer, [geom]) for layer in layerdef.layers]
    return ls, exterior[0]


def find_outer(ls, minpoint):
    import popupcad.algorithms.points as points
    lsouter = Laminate(ls.layerdef)
    lsinner = Laminate(ls.layerdef)
    for layer, layer_geometry in ls.layer_sequence.items():
        outergeoms = []
        innergeoms = []
        for geom in layer_geometry.geoms:
            if points.pointinpoints(
                    minpoint,
                    popupcad.algorithms.csg_shapely.to_generic(geom).exteriorpoints(scaling = popupcad.csg_processing_scaling),
                    popupcad.distinguishable_number_difference):
                outergeoms.append(geom)
            else:
                innergeoms.append(geom)
        lsouter.replacelayergeoms(layer, outergeoms)
        lsinner.replacelayergeoms(layer, innergeoms)
    return lsouter, lsinner


def firstpass(robot, keepout, layerdef):
    firstpass = keepout.difference(robot)
    return firstpass


def generate_web(robot, keepout, layerdef, value_outer, value_inner):
    buffered_keepout = keepout.buffer(value_inner)
    robot_support, minpoint = supportsheet(layerdef, robot, value_outer)
    buffered_web = robot_support.difference(buffered_keepout)
    outer_web, inner_elements = find_outer(buffered_web, minpoint)
    return robot_support, outer_web, inner_elements, buffered_keepout


def autosupport(robot, keepout, layerdef, value_inner, value_gap, cut_out):
    import popupcad
    cleanup = 1e-3 *popupcad.csg_processing_scaling
    buffered_keepout = keepout.buffer(value_inner)
    allsupport = buffered_keepout.difference(keepout)
    invalidsupport = keepout.difference(robot)
    buffered_invalidsupport = invalidsupport.buffer(-cleanup)
    buffered_invalidsupport = buffered_invalidsupport.buffer(
        value_gap +
        cleanup)
    valid_support = allsupport.difference(buffered_invalidsupport)
    buffered_valid_support = valid_support.buffer(cleanup)
    k2 = keepout.buffer(cut_out)
    k3 = k2.difference(keepout)
    return buffered_valid_support, k3
