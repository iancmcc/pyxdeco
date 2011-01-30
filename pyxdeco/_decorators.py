import functools
from .advice import addClassAdvisor


class _BaseDecorator(object):
    def __init__(self, func):
        self.__wrapped__ = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        return self.get_decorated_func()(*args, **kwargs)

    def get_decorated_func(self):
        return self.__wrapped__


class ClassLevelDecorator(_BaseDecorator):
    def __init__(self, func):
        def advisor(cls):
            self.decorate(func.__get__(None, cls), cls)
            return cls
        addClassAdvisor(advisor)
        super(ClassLevelDecorator, self).__init__(func)

    def decorate(self, method, cls):
        raise NotImplementedError("ClassLevelDecorator.decorate must "
                                  "be implemented in a subclass")


class InstanceLevelDecorator(_BaseDecorator):
    def __init__(self, func):
        decorate = self.decorate
        def advisor(cls):
            def decorated_init(init):
                def __init__(self, *args, **kwargs):
                    decorate(func.__get__(self, cls), self, cls)
                    init(self, *args, **kwargs)
                return __init__
            cls.__init__ = decorated_init(cls.__init__)
            return cls
        addClassAdvisor(advisor)
        super(InstanceLevelDecorator, self).__init__(func)

    def decorate(self, method, instance, cls):
        raise NotImplementedError("ClassLevelDecorator.decorate must "
                                  "be implemented in a subclass")


class MethodLevelDecorator(_BaseDecorator):
    def __new__(cls, func):
        decorator = super(MethodLevelDecorator, cls).__new__(cls)
        decorator.__init__(func)

        @functools.wraps(decorator)
        def inner(*args, **kwargs):
            return decorator(*args, **kwargs)

        return inner

    def __call__(self, *args, **kwargs):
        instance, args = args[0], args[1:]
        func = self.get_decorated_func().__get__(instance, instance.__class__)
        return self.decorate(func, *args, **kwargs)

    def decorate(self, method, *args, **kwargs):
        raise NotImplementedError("MethodLevelDecorator.decorate must "
                                  "be implemented in a subclass")


def _create_metadecorator(cls):
    def _factory(f):
        def newf(*args, **kwargs):
            return f(*args[1:], **kwargs)
        decorator = type(f.__name__, (cls,), {'decorate':newf})
        #functools.update_wrapper(decorator, f)
        return decorator
    return _factory


method_level_decorator = _create_metadecorator(MethodLevelDecorator)
instance_level_decorator = _create_metadecorator(InstanceLevelDecorator)
class_level_decorator = _create_metadecorator(ClassLevelDecorator)
