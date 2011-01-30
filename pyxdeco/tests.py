import doctest
import os.path
import unittest
from pyxdeco import ClassLevelDecorator, InstanceLevelDecorator, MethodLevelDecorator
from pyxdeco import class_level_decorator, instance_level_decorator, method_level_decorator

def mark(ob, attr='seen'):
    setattr(ob, attr, getattr(ob, attr, 0) + 1)


class TestClassLevel(ClassLevelDecorator):

    def decorate(self, method, cls):
        mark(cls)
        mark(method.im_func)


class TestInstanceLevel(InstanceLevelDecorator):

    def decorate(self, method, instance, cls):
        mark(instance, 'inst_seen')
        mark(cls, 'inst_seen')
        mark(method.im_func, 'inst_seen')


class TestMethodLevel(MethodLevelDecorator):

    def decorate(self, method, *args, **kwargs):
        mark(method.im_func, 'meth_seen')
        return method(*args, **kwargs)


class TestableClass(object):

    @TestClassLevel
    def classlevel(self):
        pass

    @TestInstanceLevel
    def instancelevel(self):
        pass

    @TestMethodLevel
    def methodlevel(self, a):
        return a**2


class TestDecorators(unittest.TestCase):

    def tearDown(self):
        TestableClass.inst_seen = 0
        TestableClass.instancelevel.__wrapped__.inst_seen = 0

    def test_classlevel(self):
        # Once from class definition
        self.assertEqual(getattr(TestableClass, 'seen', 0), 1)
        inst = TestableClass()
        self.assertEqual(getattr(inst.classlevel.__wrapped__, 'seen', 0), 1)
        inst2 = TestableClass()
        self.assertEqual(getattr(inst.classlevel.__wrapped__, 'seen', 0), 1)

    def test_instancelevel(self):
        inst = TestableClass()
        self.assertEqual(getattr(inst, 'inst_seen', 0), 1)
        self.assertEqual(getattr(TestableClass, 'inst_seen', 0), 1)
        self.assertEqual(getattr(inst.instancelevel.__wrapped__, 'inst_seen', 0), 1)

        inst2 = TestableClass()
        self.assertEqual(getattr(inst2, 'inst_seen', 0), 2)
        self.assertEqual(getattr(TestableClass, 'inst_seen', 0), 2)
        self.assertEqual(getattr(inst.instancelevel.__wrapped__, 'inst_seen', 0), 2)

    def test_methodlevel(self):
        inst = TestableClass()
        result = inst.methodlevel(2)
        self.assertEqual(4, result)
        self.assertEqual(getattr(inst.methodlevel.__wrapped__, 'meth_seen', 0), 1)
        result = inst.methodlevel(3)
        self.assertEqual(9, result)
        self.assertEqual(getattr(inst.methodlevel.__wrapped__, 'meth_seen', 0), 2)

    def test_func_decorator(self):
        x = []
        class MyDecorator(MethodLevelDecorator):
            def decorate(self, func, *args, **kwargs):
                x.append(True)
                return func(*args, **kwargs)

        @MyDecorator
        def squared(n):
            return n**2

        result = squared(2)
        self.assertEqual(4, result)
        self.assertEqual(len(x), 1)
        self.assertEqual(x[0], True)

    def test_decorator_factories(self):
        seen = {}

        @method_level_decorator
        def method_level(f, *args, **kwargs):
            seen['method'] = True
            return f(*args, **kwargs)

        @instance_level_decorator
        def instance_level(f, inst, cls):
            seen['instance'] = True

        @class_level_decorator
        def class_level(f, cls):
            seen['class'] = True

        KEYS = ('method', 'instance', 'class')

        for k in KEYS:
            self.assertEqual(seen.get(k), None)

        class Thing(object):

            @class_level
            def a(self):
                pass

            @instance_level
            def b(self):
                pass

            @method_level
            def c(self):
                pass

        self.assertEqual(seen.get('class'), True)
        self.assertEqual(seen.get('instance'), None)
        self.assertEqual(seen.get('method'), None)

        t = Thing()

        self.assertEqual(seen.get('instance'), True)
        self.assertEqual(seen.get('method'), None)

        t.c()

        self.assertEqual(seen.get('method'), True)


if __name__=="__main__":
    testfile = os.path.join(os.path.dirname(__file__), '..', 'README.rst')
    doctest.testfile(testfile)
    unittest.main()

