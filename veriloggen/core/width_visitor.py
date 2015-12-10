from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import copy

import veriloggen.core.vtypes as vtypes

class WidthVisitor(object):
    def __init__(self, prefix=None, postfix=None):
        self.prefix = prefix if prefix is not None else ''
        self.postfix = postfix if postfix is not None else ''
        
    def generic_visit(self, node):
        raise TypeError("Type %s is not supported." % str(type(node)))
    
    def visit(self, node):
        if node is None: return None
        if isinstance(node, vtypes._Variable):
            return self.visit__Variable(node)
        if isinstance(node, vtypes._BinaryOperator):
            return self.visit__BinaryOperator(node)
        if isinstance(node, vtypes._UnaryOperator):
            return self.visit__UnaryOperator(node)
        
        visitor = getattr(self, 'visit_' + node.__class__.__name__, self.generic_visit)
        return visitor(node)

    def visit__Variable(self, node):
        ret = copy.deepcopy(node)
        ret.name = ''.join([self.prefix, ret.name, self.postfix])
        return ret

    def visit_Pointer(self, node):
        var = self.visit(node.var)
        pos = self.visit(node.pos)
        return vtypes.Pointer(var, pos)

    def visit_Slice(self, node):
        var = self.visit(node.var)
        msb = self.visit(node.msb)
        lsb = self.visit(node.lsb)
        return vtypes.Slice(var, msb, lsb)

    def visit_Cat(self, node):
        vars = [ self.visit(var) for var in node.vars ]
        return vtypes.Cat(*vars)

    def visit_Repeat(self, node):
        var = self.visit(node.var)
        times = self.visit(node.times)
        return vtypes.Repeat(var, times)
    
    def visit__BinaryOperator(self, node):
        op = type(node)
        left = self.visit(node)
        right = self.visit(right)
        return op(left, right)
    
    def visit__UnaryOperator(self, node):
        op = type(node)
        right = self.visit(right)
        return op(right)
