import logging
from dataclasses import dataclass
from functools import wraps

logging.basicConfig(level=logging.DEBUG)


def log_class(level, captured_methods: list[str], logger_name: str = ""):
    def _log_class(cls):
        for captured_method in captured_methods:
            if captured_method in vars(cls) and callable(vars(cls)[captured_method]):
                _method = vars(cls)[captured_method]
                setattr(cls, captured_method, log_function(level, logger_name, method_prefix=cls.__name__)(_method))
        return cls
    return _log_class


def log_function(level, logger_name: str = "", method_prefix: str = ""):
    def _log_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            prefix = "function: " if method_prefix == "" else f"method: {method_prefix}."
            args_str = ""
            _args = args[1:] if method_prefix else args
            for arg in _args:
                args_str += f"{arg}, "
            kwargs_str = ""
            for k, v in kwargs.items():
                kwargs_str += f"{k}={v}, "
            _logger = logging.getLogger(logger_name)
            _logger.log(level, "Calling %s%s(%s)", prefix, func.__name__, args_str + kwargs_str)
            result = func(*args, **kwargs)
            _logger.log(level, "Result: %s", result)
            return result
        return wrapper
    return _log_function


@log_class(level=logging.INFO, captured_methods=["foo", "bar"], logger_name="Foo")
@dataclass
class Foo:
    count: int = 1

    def foo(self):
        """foo
        """
        pass

    def bar(self, my_arg: float, **kwargs) -> str:
        """bar

        Args:
            my_arg (float): _description_

        Returns:
            str: _description_
        """
        return f"{self.count} --- {my_arg}"

@log_function(level=logging.DEBUG, logger_name="Foo")
def baz(a: int, b: float) -> tuple[str, int]:
    return f"{a+b}", int(a*b)

def main():
    logging.debug("Start main")
    foo = Foo()
    logging.debug("Foo object %s", foo)
    res = foo.bar(2.0, baz="BAZ")
    print(res)
    foo.foo()
    baz(12, 1.5)

if __name__ == "__main__":
    main()