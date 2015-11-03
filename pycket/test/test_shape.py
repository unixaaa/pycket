#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Test.
#
import sys
import py


# from pycket.execution import *
from pycket.shape import *
from pycket.values import *
from pycket.values_struct import *

# from pycket.expression import *
# from pycket.util.construction_helper import (pattern, cons, integer, expression,
#                                            ziprules, pycket, mu,
#                                            nil, is_nil,
#                                            conslist, plist,
#                                            execution_stack)

# compat
def integer(x):return W_Fixnum(x)
def sym(x): return W_Symbol.make(x)

def w_structtype(
        name, super=w_false, init_field_cnt=integer(0),
        auto_field_cnt=integer(0), auto_v=values.w_false,
        inspector=values.w_false, proc_spec=values.w_false,
        immutables=values.w_null, guard=values.w_false,
        constr_name=values.w_false):
    return W_StructType(
        name, super, init_field_cnt, auto_field_cnt,
        auto_v, inspector, proc_spec, immutables, guard, constr_name)

_nil_tag = struct_tag("nil", 0, w_structtype(sym("nil"), w_false, integer(0)))
_w_nil = W_NAryStruct(_nil_tag.default_shape)
_w_nil._init_storage([])
def nil(): return _w_nil
def is_nil(o): return isinstance(o, W_NAryStruct) and o.get_tag is struct_tag("nil", 0)

def clean_tag(name=None, arity=None, type=None):
    from pycket.shape import _Tag
    if type is not None:
        return StructTag(type)
    else:
        w_st = w_structtype(
            name=sym(name), init_field_cnt=integer(arity))
        return StructTag(w_st)

class SConf(object):
    def __init__(self, **kwargs):
        self._config = kwargs
        self._orig_config = None
    def __enter__(self):
        self._orig_config = CompoundShape._config
        CompoundShape._config = ShapeConfig()
        for key, val in self._orig_config.__dict__.items():
            setattr(CompoundShape._config, key, val)
        for key, val in self._config.items():
            setattr(CompoundShape._config, key, val)
    def __exit__(self, type, value, traceback):
        CompoundShape._config = self._orig_config


class TestShapeAccess(object):

    def test_simple_predefined_shape(self):

        w_1 = integer(1)
        barf_0 = clean_tag("barf", 0)
        shape = CompoundShape(barf_0, [])
        c = W_NAryStruct(shape)
        c._init_storage([])
        assert c.get_number_of_children() == 0

        barf_1 = clean_tag("barf", 1)
        shape = CompoundShape(barf_1, [in_storage_shape])
        c = W_NAryStruct(shape)
        c._init_storage([w_1])
        assert c.get_number_of_children() == 1
        assert c.get_child(0) == w_1

        barf_2 = clean_tag("barf", 2)
        shape = CompoundShape(barf_2, [in_storage_shape] * 2)
        c = W_NAryStruct(shape)
        c._init_storage([w_1, w_1])
        assert c.get_number_of_children() == 2
        assert c.get_child(0) == w_1
        assert c.get_child(1) == w_1

    def test_recursive_predefined_shape(self):

        w_1 = integer(1)

        barf_1 = clean_tag("barf", 1)
        shape_1 = CompoundShape(barf_1, [in_storage_shape])
        c_1 = W_NAryStruct(shape_1)
        c_1._init_storage([w_1])
        assert c_1.get_number_of_children() == 1
        assert c_1.get_child(0) == w_1

        zork_2 = clean_tag("zork", 2)
        shape_2 = CompoundShape(zork_2, [shape_1, shape_1])
        c_1_1 = W_NAryStruct(shape_1)
        c_1_1._init_storage([w_1])
        c_2 = W_NAryStruct(shape_2)
        c_2._init_storage([w_1, w_1])
        assert c_2.get_number_of_children() == 2
        assert c_2.get_child(0) == c_1
        assert c_2.get_child(0).get_child(0) == w_1
        assert c_2.get_child(1).get_child(0) == w_1

        foo_2 = clean_tag("foo", 2)
        shape_3 = CompoundShape(foo_2, [shape_2, shape_2])
        c_1_3 = W_NAryStruct(shape_1)
        c_1_3._init_storage([w_1])
        c_1_4 = W_NAryStruct(shape_1)
        c_1_4._init_storage([w_1])
        c_2_1 = W_NAryStruct(shape_2)
        c_2_1._init_storage([c_1_3, c_1_4])
        # foo(zork(barf(1),barf(1)),zork(barf(1),barf(1)))
        c_3 = W_NAryStruct(shape_3)
        c_3._init_storage([w_1,w_1,w_1,w_1])
        assert c_3.get_number_of_children() == 2

        assert c_3.get_child(0) == c_2
        assert c_3.get_child(0).get_child(0) == c_1
        assert c_3.get_child(0).get_child(0).get_child(0) == w_1
        assert c_3.get_child(0).get_child(1) == c_1
        assert c_3.get_child(0).get_child(1).get_child(0) == w_1
        assert c_3.get_child(1).get_child(0).get_child(0) == w_1
        assert c_3.get_child(1).get_child(1).get_child(0) == w_1

    def test_recursive_mixed_predefined_shape(self):

        w_1 = integer(1)

        barf_1 = clean_tag("barf", 1)
        shape_1 = CompoundShape(barf_1, [in_storage_shape])
        c_1 = W_NAryStruct(shape_1)
        c_1._init_storage([w_1])
        assert c_1.get_number_of_children() == 1
        assert c_1.get_child(0) == w_1

        zork_2 = clean_tag("zork", 2)
        shape_2 = CompoundShape(zork_2, [shape_1, shape_1])
        c_1_1 = W_NAryStruct(shape_1)
        c_1_1._init_storage([w_1])
        c_2 = W_NAryStruct(shape_2)
        c_2._init_storage([w_1, w_1])
        assert c_2.get_number_of_children() == 2
        assert c_2.get_child(0) == c_1
        assert c_2.get_child(0).get_child(0) == w_1
        assert c_2.get_child(1).get_child(0) == w_1


        foo_2 = clean_tag("foo", 2)
        # foo(zork(barf(1),barf(1)),zork(barf(1),barf(1)))
        shape_3 = CompoundShape(foo_2, [
                        CompoundShape(zork_2, [
                            shape_1,
                            in_storage_shape]),
                        in_storage_shape])
        c_1_3 = W_NAryStruct(shape_1)
        c_1_3._init_storage([w_1])
        c_1_4 = W_NAryStruct(shape_1)
        c_1_4._init_storage([w_1])
        s_2_1 = CompoundShape(zork_2, [in_storage_shape, in_storage_shape])
        c_2_1 = W_NAryStruct(s_2_1)
        c_2_1._init_storage([c_1_3, c_1_4])

        # DIFFERENCE TO other test: not everything is flattened
        c_3 = W_NAryStruct(shape_3)
        c_3._init_storage([
            # zork
            w_1,c_1_1,
            # zork
            c_2_1])
        assert c_3.get_number_of_children() == 2
        assert c_3.get_child(0) == c_2
        assert c_3.get_child(0).get_child(0) == c_1
        assert c_3.get_child(0).get_child(0).get_child(0) == w_1
        assert c_3.get_child(0).get_child(1) == c_1
        assert c_3.get_child(0).get_child(1).get_child(0) == w_1
        assert c_3.get_child(1).get_child(0).get_child(0) == w_1
        assert c_3.get_child(1).get_child(1).get_child(0) == w_1


class TestShapeMerger(object):
    u"""
    A Shape Merger takes the tag and new children of a to-be built
    constructor and tries to match wether the emerging shape and the
    existing shape have some form of transformation to a new shape.
    This shape is then used for building the constructor
    """

    def test_splice(self):
        from pycket.shape import _splice

        a = [1, 2, 3]
        len_a = len(a)
        b = [4, 5]
        len_b = len(b)
        c = []
        len_c = len(c)
        d = [6]
        len_d = len(d)
        x = _splice(a, len_a, 1, b, len_b)
        assert x == [1, 4 ,5, 3]

        y = _splice(a, len_a, 1, c, len_c)
        assert y == [1, 3]

        z = _splice(a, len_a, 1, d, len_d)
        assert z == [1, 6, 3]

        u = _splice(a, len_a, 0, d, len_d)
        assert u == [6, 2, 3]

        v = _splice(a,len_a,  0, b, len_b)
        assert v == [4, 5, 2, 3]

        w = _splice(a, len_a, 2, b, len_b)
        assert w == [1, 2, 4, 5]


    def test_simple_shape_non_merge(self):
        w_1 = integer(1)
        barf_0 = clean_tag("barf", 0)
        shape_0 = CompoundShape(barf_0, [])
        storage = []
        (new_shape, new_storage) = shape_0.fusion(storage)
        assert new_shape == shape_0
        assert new_storage == storage

        w_1 = integer(1)
        barf_1 = clean_tag("barf", 1)
        shape_1 = CompoundShape(barf_1, [in_storage_shape])
        storage = [w_1]
        (new_shape, new_storage) = shape_1.fusion(storage)
        assert new_shape == shape_1
        assert new_storage == storage

    def test_compound_shape_non_merge(self):
        w_1 = integer(1)

        barf_1 = clean_tag("barf", 1)
        shape_1 = CompoundShape(barf_1, [in_storage_shape])
        c_1 = W_NAryStruct(shape_1)
        c_1._init_storage([w_1])

        zork_2 = clean_tag("zork", 2)
        shape_2 = CompoundShape(zork_2, [in_storage_shape, in_storage_shape])
        c_1_1 = W_NAryStruct(shape_1)
        c_1_1._init_storage([w_1])
        c_2 = W_NAryStruct(shape_2)
        c_2._init_storage([c_1, c_1_1])

        foo_2 = clean_tag("foo", 2)
        shape_3 = CompoundShape(foo_2, [shape_2, shape_2])
        c_1_3 = W_NAryStruct(shape_1)
        c_1_3._init_storage([w_1])
        c_1_4 = W_NAryStruct(shape_1)
        c_1_4._init_storage([w_1])
        c_2_1 = W_NAryStruct(shape_2)
        c_2_1._init_storage([c_1_3, c_1_4])

        storage = [w_1, w_1, w_1, w_1]
        (new_shape, new_storage) = shape_3.fusion(storage)
        assert new_shape == shape_3
        assert new_storage == storage


    def test_compound_shape_merge_1(self):
        """
           (zork (barf 1) (barf 1))
        """
        w_1 = integer(1)

        barf_1 = clean_tag("barf", 1)
        shape_1 = CompoundShape(barf_1, [in_storage_shape])
        c_1 = W_NAryStruct(shape_1)
        c_1._init_storage([w_1])
        c_1_1 = W_NAryStruct(shape_1)
        c_1_1._init_storage([w_1])

        zork_2 = clean_tag("zork", 2)
        shape_2 = CompoundShape(zork_2, [in_storage_shape, in_storage_shape])

        shape_2_1 = CompoundShape(zork_2, [shape_1, in_storage_shape])
        shape_2_2 = CompoundShape(zork_2, [in_storage_shape, shape_1])
        shape_2_3 = CompoundShape(zork_2, [shape_1, shape_1])

        shape_2.transformation_rules[(0, shape_1)] = shape_2_1
        shape_2.transformation_rules[(1, shape_1)] = shape_2_2

        shape_2_1.transformation_rules[(1, shape_1)] = shape_2_3

        shape_2_2.transformation_rules[(0, shape_1)] = shape_2_3

        storage = [c_1, c_1_1]

        (new_shape, new_storage) = shape_2.fusion(storage)

        assert new_shape == CompoundShape(zork_2, [shape_1, shape_1])
        assert new_storage == [w_1, w_1]

    def test_compound_shape_merge_2(self):
        """
           (foo (zork (barf 1) (barf 1)) (zork (barf 1) (barf 1)))
        """
        w_1 = integer(1)

        barf_1 = clean_tag("barf", 1)
        shape_1 = CompoundShape(barf_1, [in_storage_shape])
        c_1 = W_NAryStruct(shape_1)
        c_1._init_storage([w_1])
        c_1_1 = W_NAryStruct(shape_1)
        c_1_1._init_storage([w_1])

        zork_2 = clean_tag("zork", 2)
        shape_2 = CompoundShape(zork_2, [in_storage_shape, in_storage_shape])

        shape_2_1 = CompoundShape(zork_2, [shape_1, in_storage_shape])
        shape_2_2 = CompoundShape(zork_2, [in_storage_shape, shape_1])
        shape_2_3 = CompoundShape(zork_2, [shape_1, shape_1])

        shape_2.transformation_rules[(0, shape_1)] = shape_2_1
        shape_2.transformation_rules[(1, shape_1)] = shape_2_2

        shape_2_1.transformation_rules[(1, shape_1)] = shape_2_3

        shape_2_2.transformation_rules[(0, shape_1)] = shape_2_3

        storage = [c_1, c_1_1]

        (new_shape, new_storage) = shape_2.fusion(storage)

        c_2 = W_NAryStruct(new_shape)
        c_2._init_storage(new_storage)

        foo_2 = clean_tag("foo", 2)
        shape_3 = CompoundShape(foo_2, [shape_2_3, in_storage_shape])

        shape_3_1 = CompoundShape(foo_2, [shape_2_3, shape_2_3])

        shape_3.transformation_rules[(2, new_shape)] = shape_3_1
        storage = new_storage + [c_2]
        (new_shape, new_storage) = shape_3.fusion(storage)
        assert new_storage == [w_1, w_1, w_1, w_1]
        assert new_shape == CompoundShape(foo_2, [shape_2_3, shape_2_3])

    def test_cons_list(self):

        w_1 = integer(1)

        cons_ = clean_tag("cons", 2)

        nil_ = clean_tag("nil", 0)
        nil_shape = CompoundShape(nil_, [])
        w_nil_ = W_NAryStruct(nil_shape)
        w_nil_._init_storage([])

        list_default_shape = CompoundShape(cons_, [in_storage_shape, in_storage_shape])

        list_1_shape = CompoundShape(cons_, [in_storage_shape, nil_shape])
        list_2_shape = CompoundShape(cons_, [in_storage_shape, list_1_shape])

        list_default_shape.transformation_rules[(1,nil_shape)] = list_1_shape
        list_default_shape.transformation_rules[(1,list_1_shape)] = list_2_shape

        w_list_0 = w_nil_

        (shape, storage) = list_default_shape.fusion([w_1, w_nil_])

        w_list_1 = W_NAryStruct(shape)
        w_list_1._init_storage(storage)

        list_1_shape.transformation_rules[(1, list_1_shape)] = list_2_shape

        (shape, storage) = list_default_shape.fusion([w_1, w_list_1])

        w_list_2 = W_NAryStruct(shape)
        w_list_2._init_storage(storage)

        assert w_list_2._storage == [w_1, w_1]

    # def test_reverse(self):

    #     debug = False

    #     if debug:
    #         print ""

    #     c = clean_tag("cons", 2)
    #     def _cons(*children):
    #         ch = list(children)
    #         constr = W_NAryStruct(c.default_shape)
    #         constr._init_storage(ch)
    #         return constr
    #     def _conslist(p_list):
    #         result = nil()
    #         for element in reversed(p_list):
    #             result = _cons(element, result)
    #         return result

    #     cons_shape = c.default_shape
    #     with SConf(substitution_threshold=sys.maxint):
    #         cons_1_shape = CompoundShape(c, [in_storage_shape, cons_shape ])
    #         cons_2_shape = CompoundShape(c, [in_storage_shape, cons_1_shape])
    #         cons_3_shape = CompoundShape(c, [in_storage_shape, cons_2_shape])
    #         cons_4_shape = CompoundShape(c, [in_storage_shape, cons_3_shape])
    #         cons_5_shape = CompoundShape(c, [in_storage_shape, cons_4_shape])
    #         cons_1_shape._config.substitution_threshold = sys.maxint
    #         cons_2_shape._config.substitution_threshold = sys.maxint
    #         cons_3_shape._config.substitution_threshold = sys.maxint
    #         cons_4_shape._config.substitution_threshold = sys.maxint
    #         cons_5_shape._config.substitution_threshold = sys.maxint
    #         cons_shape.transformation_rules[(1, cons_shape )] = cons_1_shape
    #         cons_shape.transformation_rules[(1, cons_1_shape)] = cons_2_shape
    #         cons_shape.transformation_rules[(1, cons_2_shape)] = cons_3_shape
    #         # cons_shape.transformation_rules[(1, cons_3_shape)] = cons_4_shape
    #         # cons_shape.transformation_rules[(1, cons_4_shape)] = cons_5_shape

    #         cons_1_shape.transformation_rules[(1, cons_1_shape)] = cons_2_shape
    #         cons_1_shape.transformation_rules[(1, cons_2_shape)] = cons_3_shape
    #         # cons_1_shape.transformation_rules[(1, cons_3_shape)] = cons_4_shape
    #         # cons_1_shape.transformation_rules[(1, cons_4_shape)] = cons_5_shape

    #         cons_2_shape.transformation_rules[(1, cons_2_shape)] = cons_3_shape
    #         # cons_2_shape.transformation_rules[(1, cons_3_shape)] = cons_4_shape
    #         # cons_2_shape.transformation_rules[(1, cons_4_shape)] = cons_5_shape

    #         # cons_3_shape.transformation_rules[(1, cons_3_shape)] = cons_4_shape
    #         # cons_3_shape.transformation_rules[(1, cons_4_shape)] = cons_5_shape

    #         # cons_4_shape.transformation_rules[(1, cons_4_shape)] = cons_5_shape

    #         reverse_acc = lamb()
    #         reverse_acc._name ="reverse_acc"
    #         reverse_acc._rules = ziprules(
    #             ([nil(),       a1], a1),
    #             ([_cons(h, t), a2], mu(reverse_acc, [t, _cons(h, a2)])),
    #         )

    #         l = Variable("l")
    #         reverse = lamb(([l], mu(reverse_acc, [l, nil()])))
    #         reverse._name = "reverse"

    #         def stackinspect(d):

    #             from lamb.util.debug import storagewalker

    #             op_stack = d['op_stack']
    #             ex_stack = d['ex_stack']

    #             if op_stack:
    #                 if isinstance(op_stack._data, W_Struct):
    #                     print "[W]", op_stack._data._shape,
    #                     print " storage: ",
    #                     print storagewalker(op_stack._data.get_storage())
    #                 else:
    #                     print "[W]", op_stack._data
    #             else:
    #                 print "[w] none"


    #         nums = 50
    #         list1_w = [integer(x) for x in range(nums)]
    #         clist1_w = _conslist(list1_w)
    #         assert clist1_w.get_tag() is c

    #         res = interpret(execution_stack(mu(reverse, [clist1_w])))
    #         list1_w.reverse()
    #         assert plist(res) == list1_w

    # def test_plus(self):
    #     from mu.peano import peano_num, python_num, startup_peano, _plus
    #     startup_peano()

    #     n = 10
    #     # n = 100
    #     arg1 = peano_num(n)
    #     assert python_num(arg1) == n

    #     arg2 = peano_num(n)
    #     assert python_num(arg2) == n

    #     stack_e = execution_stack(mu(_plus(), [arg1, arg2]))
    #     assert python_num(arg2) == n
    #     assert python_num(arg1) == n

    #     res = interpret(stack_e)
    #     assert python_num(arg2) == n
    #     assert python_num(arg1) == n
    #     assert python_num(res) == n + n


    # def test_mult(self):
    #     from mu.peano import peano_num, python_num, startup_peano, _mult
    #     startup_peano()

    #     n = 4
    #     # n = 100
    #     arg1 = peano_num(n)
    #     assert python_num(arg1) == n

    #     arg2 = peano_num(n)
    #     assert python_num(arg2) == n

    #     stack_e = execution_stack(mu(_mult(), [arg1, arg2]))
    #     assert python_num(arg2) == n
    #     assert python_num(arg1) == n

    #     print "\n" * 10

    #     res = interpret(stack_e)
    #     assert python_num(arg2) == n
    #     assert python_num(arg1) == n
    #     assert python_num(res) == n * n



class TestShapeRecorder(object):

    def test_simple_record(self):
        w_1 = integer(1)
        ferb_1 = clean_tag("ferb_0", 1)
        s = ferb_1.default_shape

        children = [w_1]
        new_shape, new_storage = s.merge(children)
        # s.record_shapes(new_storage)

        assert s._hist == {}

        children = [nil()]
        new_shape, new_storage = s.merge(children)
        # s.record_shapes(new_storage)

        assert s._hist == {
            (0, nil()._shape): 1,
        }

    def test_simple_autosubstitution(self):
        with SConf(substitution_threshold=2):

            ferb_1 = clean_tag("ferb_1", 1)
            shape = ferb_1.default_shape

            children = [nil()]
            new_shape, new_storage = shape.merge(children)
            # shape.record_shapes(new_storage)

            assert shape._hist == {
                (0, nil()._shape):  1,
            }
            assert new_shape is shape

            c = W_NAryStruct(new_shape)
            c._init_storage(new_storage)

            children_1 = [c]
            new_shape_1, new_storage_1 = shape.merge(children_1)
            # shape.record_shapes(new_storage_1)

            assert shape._hist == {
                (0, nil()._shape):  1,
                (0, shape): 1,
            }
            assert new_shape_1 is shape

            children_2 = [c]
            new_shape_2, new_storage_2 = shape.merge(children_2)
            # shape.record_shapes(new_shape_1, new_storage_1)

            # assert len(shape._hist) > 1
            assert new_shape_2 is not shape


    def test_counting(self):

        zork_2 = clean_tag("zork_2", 2)
        shape = zork_2.default_shape

        c = W_NAryStruct(shape)
        c._init_storage([nil(), nil()])

        shape.record_shapes([c, c])

        assert shape._hist == {
            (0, shape): 1,
            (1, shape): 1,
        }


class TestShapeRecognizer(object):

    def test_recognize_unary_transformation(self):

        ferb_1 = clean_tag("ferb_1", 1)
        shape = ferb_1.default_shape

        children = [nil()]
        new_shape, new_storage = shape.merge(children)

        assert new_shape is shape
        assert new_storage == children
        shape.recognize_transformation(0, nil()._shape)


        new_shape, new_storage = shape.merge(children)

        assert shape.transformation_rules == {
            (0, nil()._shape): new_shape,
        }

        assert new_shape is not shape
        assert new_storage == []

        shape.recognize_transformation(0, shape)

        c = W_NAryStruct(shape)
        c._init_storage(children)


        children_1 = [c]
        new_shape_1, new_storage_1 = shape.merge(children_1)

        assert shape.transformation_rules == {
            (0, nil()._shape): new_shape,
            (0, shape): new_shape_1,
        }

        assert new_shape_1 is not shape
        assert new_shape_1 is not new_shape
        assert new_storage_1 == children

    def test_recognize_recursive_shapes(self):

        ferb_2 = clean_tag("ferb_2", 2)
        shape = ferb_2.default_shape

        c_shape = CompoundShape(ferb_2, [in_storage_shape, shape])

        c_shape.recognize_transformation(2, shape)

        new_shape = c_shape.transformation_rules[2, shape]

        assert new_shape._structure[0] == in_storage_shape
        subshape = new_shape._structure[1]
        assert subshape._structure[0] == in_storage_shape
        assert subshape._structure[1] is shape

    def test_replace_subshapes(self):


        ferb_2 = clean_tag("ferb_2", 2)
        shape = ferb_2.default_shape

        c_shape = CompoundShape(ferb_2, [in_storage_shape, shape])

        assert in_storage_shape.replace(0, shape) is shape

        new_structure = shape.replace(1, shape)._structure
        assert new_structure[0] is in_storage_shape
        assert new_structure[1] is shape


        new_shape = c_shape.replace(2, shape)
        assert new_shape._structure[0] == in_storage_shape
        subshape = new_shape._structure[1]
        assert subshape._structure[0] == in_storage_shape
        assert subshape._structure[1] is shape

    def test_recognize_deep_structures(self):
        w_1 = integer(1)
        c = clean_tag("cons", 2)

        def _cons(*children):
            ch = list(children)
            pre_shape = c.default_shape
            shape, storage = pre_shape.fusion(children)
            constr = W_NAryStruct(shape)
            constr._init_storage(storage)
            return constr
        def _conslist(p_list):
            result = nil()
            for element in reversed(p_list):
                result = _cons(element, result)
            return result

        with SConf(substitution_threshold = 2):

            # print ""
            cons_0 = _cons(w_1, nil())
            assert cons_0.shape() == c.default_shape
            print cons_0.shape()
            print c.default_shape._hist
            assert c.default_shape.transformation_rules == {}

            cons_1 = _cons(w_1, cons_0)
            assert cons_1.shape() == c.default_shape
            assert cons_1.shape() == cons_0.shape()
            print cons_1.shape()
            print c.default_shape._hist
            assert c.default_shape.transformation_rules == {}

            cons_2 = _cons(w_1, cons_1)
            assert cons_2.shape() != c.default_shape
            assert cons_2.shape() != cons_0.shape()
            assert cons_2.shape() != cons_1.shape()
            print cons_2.shape()
            print c.default_shape._hist
            assert c.default_shape.transformation_rules == {
                (1, c.default_shape): cons_2.shape(),
            }

            cons_3 = _cons(w_1, cons_2)
            print cons_3.shape()
            print c.default_shape._hist
            assert c.default_shape.transformation_rules == {
                (1, c.default_shape): cons_2.shape(),
            }

            cons_4 = _cons(w_1, cons_3)
            print cons_4.shape()
            print c.default_shape._hist
            assert c.default_shape.transformation_rules == {
                (1, c.default_shape): cons_2.shape(),
            }

            cons_5 = _cons(w_1, cons_4)
            print cons_5.shape()
            print c.default_shape._hist
            assert c.default_shape.transformation_rules == {
                (1, c.default_shape): cons_2.shape(),
                (1, cons_2.shape()): cons_5.shape(),
            }


    def test_bounded_deep_structures(self):
        w_1 = integer(1)
        c = clean_tag("cons", 2)

        def _cons(*ch):
            children = list(ch)
            pre_shape = c.default_shape
            shape, storage = pre_shape.fusion(children)
            constr = W_NAryStruct(shape)
            constr._init_storage(storage)
            return constr
        def _conslist(p_list):
            result = nil()
            for element in reversed(p_list):
                result = _cons(element, result)
            return result

        with SConf(substitution_threshold = 17):

            def check_width(c, width):
                if isinstance(c, W_Struct) and not is_nil(c):
                    assert c.get_storage_width() < width
                    # We deliberately use a n-ary Struct, hence,
                    # know that _structure is there
                    for child in c._storage:
                        check_width(child, width)

            sys.setrecursionlimit(100000)
            for num in [50, 100, 1000, 10000, 50000]:
                l = _cons(w_1, nil())
                for i in range(num):
                    l = _cons(w_1, l)
                check_width(l, 25)

    def test_bounded_shallow_deep_structures(self):
        e = clean_tag("E", 0)
        def _e():
            pre_shape = e.default_shape
            shape, storage = pre_shape.fusion([])
            constr = W_NAryStruct(shape)
            constr._init_storage(storage)
            return constr

        with SConf(substitution_threshold = 17, max_shape_depth = 7):

            sys.setrecursionlimit(100000)
            for num in [50, 100, 1000, 10000, 50000]:
                c = clean_tag("%d_cons" % num, 2)

                def _cons(*ch):
                    children = list(ch)
                    pre_shape = c.default_shape
                    shape, storage = pre_shape.fusion(children)
                    constr = W_NAryStruct(shape)
                    constr._init_storage(storage)
                    return constr

                l = nil()
                for i in range(num):
                    l = _cons(_e(), l)
                assert l.shape().shape_depth() <= 7

    def test_post_recursive_structures(self):

        c = clean_tag("cons", 2)
        def _cons(car, cdr):
            children = [car, cdr]
            pre_shape = c.default_shape
            shape, storage = pre_shape.fusion(children)
            constr = W_NAryStruct(shape)
            constr._init_storage(storage)
            return constr

        # Be near immediate
        with SConf(substitution_threshold = 2):

            assert len(c.default_shape.transformation_rules) == 0
            assert len(c.default_shape._hist) == 0

            cell = _cons(integer(1), nil())

            assert len(c.default_shape.transformation_rules) == 0
            assert len(c.default_shape._hist) == 1

            cell2 = _cons(integer(1), cell)

            assert len(c.default_shape.transformation_rules) == 0
            assert len(c.default_shape._hist) == 2

            cell3 = _cons(integer(1), cell2)

            assert len(c.default_shape.transformation_rules) == 1
            assert len(c.default_shape._hist) == 2

            condition, result_shape = \
              c.default_shape.transformation_rules.items()[0]
            assert condition[0] == 1 # pos
            assert condition[1] is c.default_shape # shape

            assert result_shape._tag is c # same tag
            assert len(result_shape._structure) == 2
            assert result_shape._structure[0] is in_storage_shape
            assert result_shape._structure[1] is c.default_shape

            assert cell3._shape is result_shape

    def test_pre_recursive_structures(self):

        c = clean_tag("cons", 2)
        def _cons(car, cdr):
            children = [car, cdr]
            pre_shape = c.default_shape
            shape, storage = pre_shape.fusion(children)
            constr = W_NAryStruct(shape)
            constr._init_storage(storage)
            return constr

        # Be near immediate
        with SConf(substitution_threshold = 2):
            assert len(c.default_shape.transformation_rules) == 0
            assert len(c.default_shape._hist) == 0

            cell = _cons(nil(), integer(1))

            assert len(c.default_shape.transformation_rules) == 0
            assert len(c.default_shape._hist) == 1

            cell2 = _cons(cell, integer(1))

            assert len(c.default_shape.transformation_rules) == 0
            assert len(c.default_shape._hist) == 2

            cell3 = _cons(cell2, integer(1))

            assert len(c.default_shape.transformation_rules) == 1
            assert len(c.default_shape._hist) == 2

            condition, result_shape =  \
              c.default_shape.transformation_rules.items()[0]
            assert condition[0] == 0 # pos
            assert condition[1] is c.default_shape # shape

            assert result_shape._tag is c # same tag
            assert len(result_shape._structure) == 2
            assert result_shape._structure[0] is c.default_shape
            assert result_shape._structure[1] is in_storage_shape

            assert cell3._shape is result_shape

    def test_pre_constr_recursive_structures(self):

        c = clean_tag("cons", 2)
        e = clean_tag("E", 0)
        def _cons(car, cdr):
            children = [car, cdr]
            pre_shape = c.default_shape
            shape, storage = pre_shape.fusion(children)
            constr = W_NAryStruct(shape)
            constr._init_storage(storage)
            return constr
        def _e():
            pre_shape = e.default_shape
            shape, storage = pre_shape.fusion([])
            constr = W_NAryStruct(shape)
            constr._init_storage(storage)
            return constr

        # Be near immediate
        with SConf(substitution_threshold = 2):
                l = _cons(_cons(_cons(_cons(nil(), _e()), _e()),  _e()),  _e())
                s = l.shape()
                assert len(s._structure) == 2
                assert s._structure[1] == in_storage_shape
                s2 = s._structure[0]
                assert len(s2._structure) == 2
                assert s2._structure[0] == in_storage_shape
                assert s2._structure[1] == e.default_shape

    def test_post_constr_recursive_structures(self):

        c = clean_tag("cons", 2)
        e = clean_tag("E", 0)
        def _cons(car, cdr):
            children = [car, cdr]
            pre_shape = c.default_shape
            shape, storage = pre_shape.fusion(children)
            constr = W_NAryStruct(shape)
            constr._init_storage(storage)
            return constr
        def _e():
            pre_shape = e.default_shape
            shape, storage = pre_shape.fusion([])
            constr = W_NAryStruct(shape)
            constr._init_storage(storage)
            return constr

        # Be near immediate
        with SConf(substitution_threshold = 2):
            l = _cons(_e(), _cons(_e(), _cons(_e(), _cons(_e(), nil()))))
            s = l.shape()
            assert len(s._structure) == 2
            assert s._structure[0] == e.default_shape
            s2 = s._structure[1]
            assert len(s2._structure) == 2
            assert s2._structure[1] == in_storage_shape
            assert s2._structure[0] == e.default_shape

    def test_multi_recursive_structures(self):

        n = clean_tag("Node", 3)
        def _node(left, value, right):
            children = [left, value, right]
            pre_shape = n.default_shape
            shape, storage = pre_shape.fusion(children)
            constr = W_NAryStruct(shape)
            constr._init_storage(storage)
            return constr
        def _e(): return integer(1)

        # Be near immediate
        with SConf(substitution_threshold = 2):

            n1 = _node(
                _node(
                    _node(
                        _node(nil(), _e(), nil()),
                        _e(),
                        _node(nil(), _e(), nil())),
                    _e(),
                    _node(
                        _node(nil(), _e(), nil()),
                        _e(),
                        _node(nil(), _e(), nil()))),
                _e(),
                _node(
                    _node(
                        _node(nil(), _e(), nil()),
                        _e(),
                        _node(nil(), _e(), nil())),
                    _e(),
                    _node(
                        _node(nil(), _e(), nil()),
                        _e(),
                        _node(nil(), _e(), nil()))))
            n2 = _node(
                _node(
                    _node(
                        _node(nil(), _e(), nil()),
                        _e(),
                        _node(nil(), _e(), nil())),
                    _e(),
                    _node(
                        _node(nil(), _e(), nil()),
                        _e(),
                        _node(nil(), _e(), nil()))),
                _e(),
                _node(
                    _node(
                        _node(nil(), _e(), nil()),
                        _e(),
                        _node(nil(), _e(), nil())),
                    _e(),
                    _node(
                        _node(nil(), _e(), nil()),
                        _e(),
                        _node(nil(), _e(), nil()))))

            tree = _node(n1, _e(), n2)

            s = tree.shape()
            assert len(s._structure) == 3
            assert s._structure[0] == n.default_shape
            assert s._structure[1] == in_storage_shape
            assert s._structure[2] == n.default_shape

    def test_multi_constr_recursive_structures(self):

        print ""
        e = clean_tag("E", 0)
        def _e():
            pre_shape = e.default_shape
            shape, storage = pre_shape.fusion([])
            constr = W_NAryStruct(shape)
            constr._init_storage(storage)
            return constr

        n = clean_tag("Node", 3)
        def _node(left, value, right):
            children = [left, value, right]
            pre_shape = n.default_shape
            shape, storage = pre_shape.fusion(children)
            constr = W_NAryStruct(shape)
            constr._init_storage(storage)
            return constr

        # Be near immediate
        with SConf(substitution_threshold = 2):
            def make_tree():
                return _node(
                _node(
                    _node(
                        _node(nil(), _e(), nil()),
                        _e(),
                        _node(nil(), _e(), nil())),
                    _e(),
                    _node(
                        _node(nil(), _e(), nil()),
                        _e(),
                        _node(nil(), _e(), nil()))),
                _e(),
                _node(
                    _node(
                        _node(nil(), _e(), nil()),
                        _e(),
                        _node(nil(), _e(), nil())),
                    _e(),
                    _node(
                        _node(nil(), _e(), nil()),
                        _e(),
                        _node(nil(), _e(), nil()))))
            tree = make_tree()

        s = tree.shape()
        assert len(s._structure) == 3
        s0 = s._structure[0]
        assert s0 is not in_storage_shape
        assert s0._structure[0] is in_storage_shape
        assert s0._structure[1] is e.default_shape
        assert s0._structure[2] is in_storage_shape

        s1 = s._structure[1]
        assert s1 is in_storage_shape
        s2 = s._structure[2]
        assert s2 is in_storage_shape
