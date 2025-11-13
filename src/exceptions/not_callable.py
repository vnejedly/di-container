from typing import Type


class NotCallableException(Exception):

    def __init__(self, dependency_type: Type):
        self.dependency_type = dependency_type
        super().__init__(
            f"Creator function for service {dependency_type.__module__}.{dependency_type.__name__} is not callable"
        )
