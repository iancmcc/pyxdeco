===============================
Python eXtraordinary Decorators
===============================

Decorators in Python are limited to action when the function they wrap is
actually called. This package adds the ability to define decorators to be
called at any of the three points of the function's existence: when the
function is defined, when an instance of the class containing the function is
created, and when the function is itself called.

This enables the use of decorators to, e.g., tag deprecated methods and pull
up a report; register instance methods as listeners to events; manipulate
methods at class creation without metaclasses; and so on.

pyxdeco includes decorator base classes::

    >>> from pyxdeco import ClassLevelDecorator
    >>> from pyxdeco import InstanceLevelDecorator
    >>> from pyxdeco import MethodLevelDecorator

and factory decorators for easy creation of decorators from functions::

    >>> from pyxdeco import class_level_decorator
    >>> from pyxdeco import instance_level_decorator
    >>> from pyxdeco import method_level_decorator

Create a decorator by subclassing any of the base classes and overriding the
``decorate`` method. Alternatively, decorate a function with the factory
decorator and the function will be used as the ``decorate`` method for the
decorator.


Class-Level Decorators
======================
Class-level decorators are invoked when the class is created. They are called
with the decorated method and the class as arguments::

    >>> deprecated_methods = []
    >>>
    >>> @class_level_decorator
    ... def deprecated(func, cls):
    ...     deprecated_methods.append(func.__name__)
    ...
    >>> class A(object):
    ...
    ...     def not_deprecated(self):
    ...         pass
    ...
    ...     @deprecated
    ...     def deprecated_method(self):
    ...         pass
    ... 
    ...     @deprecated
    ...     def also_deprecated_method(self):
    ...         pass
    ...
    >>> deprecated_methods
    ['deprecated_method', 'also_deprecated_method']


Instance-Level Decorators
=========================
Instance-level decorators are invoked when an instance of the class containing
the decorated method is created (that is, after ``__init__``). The are called with the decorated instance method, the instance, and the class as arguments::

    >>> click_listeners = []
    >>>
    >>> @instance_level_decorator
    ... def onclick(func, inst, cls):
    ...     click_listeners.append('%s.%s' % (inst.id, func.__name__))
    ...
    >>> class A(object):
    ...     def __init__(self, id):
    ...         self.id = id
    ...
    ...     @onclick
    ...     def click_listener(self):
    ...         pass
    ... 
    >>> len(click_listeners) == 0
    True
    >>>
    >>> ob1 = A('ob1')
    >>> click_listeners
    ['ob1.click_listener']
    >>>
    >>> ob2 = A('ob2')
    >>> click_listeners
    ['ob1.click_listener', 'ob2.click_listener']


Method-Level Decorators
=======================
Method-level decorators are no different from ordinary decorators but are
provided for the sake of completeness and flexibility. They are passed the
decorated function (or instance method) and any arguments::

    >>> called = []
    >>>
    >>> @method_level_decorator
    ... def noticeme(func, *args, **kwargs):
    ...     called.append(func.__name__)
    ...
    >>> class A(object):
    ...     @noticeme
    ...     def amethod(self):
    ...         pass
    ...
    >>> a = A()
    >>> len(called) == 0
    True
    >>>
    >>> a.amethod()
    >>> called
    ['amethod']
    >>>
    >>> a.amethod()
    >>> called
    ['amethod', 'amethod']


