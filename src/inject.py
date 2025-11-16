from abc import ABC
from enum import Enum
from typing import Type, Any


class Inject(ABC):
    class Method(str, Enum):
        BY_TYPE: str = 'by_type'
        BY_NAME: str = 'by_name'

    method: Method

    # InjectType.BY_TYPE:
    unique_instance: bool
    default_implementation: Type | None

    # InjectType.BY_NAME:
    default_value: Any

    def __init__(self):
        raise Exception("Use TypeInject or NameInject")


class TypeInject(Inject):
    def __init__(
        self,
        unique_instance: bool = False,
        default_implementation: Type | None = None,
    ):
        self.method = self.Method.BY_TYPE
        self.unique_instance = unique_instance
        self.default_implementation = default_implementation


class NameInject(Inject):
    def __init__(
        self,
        default_value: Any = None,
    ):
        self.method = self.Method.BY_NAME
        self.default_value = default_value
