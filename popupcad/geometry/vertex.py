# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes.
Email: danaukes<at>seas.harvard.edu.
Please see LICENSE.txt for full license.
"""
   
import sympy
    
from popupcad.constraints.constraints import Variable, Constant
    
class Vertex(object):
    editable = ['pos','static','construction']
    deletable = []
    
    roundvalue = 5
    def __init__(self,position = None):

        self.id = id(self)
        self._pos = None
        self.setstatic(False)
        self.set_persistent(False)
        self.set_construction(True)
#        self.construction = False
#        self.static = False        
#        self._persistent = False

        if position !=None:
            self.setpos(position)
    def set_construction(self,test):
        self.construction = test
    def is_construction(self):
        try:
            return self.construction
        except AttributeError:
            self.construction = True
            return self.construction

    def setstatic(self,test):
        self.static = test

    def isValid(self):
        return True

    def is_persistent(self):
        try:
            self._persistent
        except AttributeError:
            self._persistent = False
        finally:
            return self._persistent

    def is_static(self):
        return self.static

    def set_persistent(self,test):
        self._persistent = test

    def __str__(self):
        return 'vertex'+str(self.id)
        
    def vertices(self):
        return [self]

    def lines(self):
        return []

    def __hash__(self):
        return self.id

    def __eq__(self,other):
        if type(self)==type(other):
            return self.id == other.id
        return False
        
    def p(self):
        if self.is_static():
            p_x = Constant(str(self)+'_x')
            p_y = Constant(str(self)+'_y')
        else:
            p_x = Variable(str(self)+'_x')
            p_y = Variable(str(self)+'_y')
        return sympy.Matrix([p_x,p_y,0])

    def setpos(self,pos):
        import numpy
        pos = numpy.array(pos)
        pos.round(self.roundvalue)
        self._pos = tuple(pos.tolist())

    def getpos(self):
        try:
            if self._pos==None:
                self._pos = self.__pos
                del self.__pos
                return self._pos
            else:
                return self._pos
        except AttributeError:
            self._pos = self.__pos
            del self.__pos
            return self._pos

    def setsymbol(self,variable,value):
        p = self.p()
        if p[0] == variable:
            self.setpos((value,self.getpos()[1]))            
        if p[1] == variable:
            self.setpos((self.getpos()[0],value))
            
    def properties(self):
        from popupcad.widgets.propertyeditor import PropertyEditor
        return PropertyEditor(self)
        
    def copy(self,identical = True):
        new = type(self)()
        return self.copy_values(new,identical)
        
    def copy_values(self,new,identical=False):
        new.setpos(self.getpos())
        new.static = self.static
        try:
            new._persistent = self._persistent
        except AttributeError:
            new._persistent = False
        if identical:
            new.id = self.id
        return new            
        
    def gen_interactive(self):
        from popupcad.graphics2d.interactivevertex import InteractiveVertex
        iv = InteractiveVertex(self)
        iv.updatefromgeneric()
        return iv

    def outputinteractive(self):
        from popupcad.graphics2d.drawingpoint import DrawingPoint
        iv = DrawingPoint(self)
        iv.updatefromgeneric()
        return iv

    def outputstatic(self,color):
        from popupcad.graphics2d.drawingpoint import StaticDrawingPoint
        iv = StaticDrawingPoint(self)
        iv.makemoveable(False)
        iv.updatefromgeneric()
        return iv

    def outputshapely(self):
        from shapely.geometry import Point
        p = Point(*self.getpos())
        return p
        
    def get_interactive(self):
        try:
            return self.interactivevertex
        except AttributeError:
            self.interactivevertex = self.gen_interactive()
            return self.interactivevertex

class ShapeVertex(Vertex):
    def exteriorpoints(self):
        return [self.getpos()]
    def interiorpoints(self):
        return []
    def gen_interactive(self):
        from popupcad.graphics2d.interactivevertex import InteractiveShapeVertex
        iv = InteractiveShapeVertex(self)
        iv.updatefromgeneric()
        return iv

class DrawnPoint(Vertex):
    def exteriorpoints(self):
        return [self.getpos()]
    def interiorpoints(self):
        return []
    def gen_interactive(self):
        from popupcad.graphics2d.drawingpoint import DrawingPoint
        iv = DrawingPoint(self)
        iv.updatefromgeneric()
        return iv

class ReferenceVertex(Vertex):
    def __init__(self,*args,**kwargs):
        super(ReferenceVertex,self).__init__(*args,**kwargs)
        self.set_persistent(True)
        self.setstatic(True)
    def gen_interactive(self):
        from popupcad.graphics2d.interactivevertex import ReferenceInteractiveVertex
        iv = ReferenceInteractiveVertex(self)
        iv.updatefromgeneric()
        return iv
#    def output_drawing_object(self):
#        from popupcad.graphics2d.drawingpoint import DrawingPoint
#        iv = DrawingPoint(self)
#        iv.updatefromgeneric()
#        return iv
