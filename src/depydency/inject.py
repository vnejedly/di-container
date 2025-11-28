from abc import ABC
from enum import Enum
from typing import Type, Any


class Inject(ABC):
    """The abstraction containing all the injection metadata defined
    by the client (class requesting a dependency)
    """
    class Method(str, Enum):
        BY_TYPE: str = 'by_type'
        BY_NAME: str = 'by_name'

    method: Method
    unique_instance: bool

    # Method.BY_TYPE:
    dependency_type: Type
    default_implementation: Type | None

    # Method.BY_NAME:
    dependency_name: str | None
    default_value: Any

    def __init__(self):
        raise Exception("Use TypeInject or NameInject")
    
    def set_dependency_id(
        self, 
        dependency_type: Type = Any, 
        dependency_name: str | None = None,
    ):
        self.dependency_type = dependency_type
        self.dependency_name = dependency_name


class TypeInject(Inject):
    """Use for tagging a dependency, which should be resolved by type
    and for setting up all client-defined configurations
    """
    def __init__(
        self,
        unique_instance: bool = False,
        default_implementation: Type | None = None,
    ):
        self.method = self.Method.BY_TYPE
        self.unique_instance = unique_instance
        self.default_implementation = default_implementation


class NameInject(Inject):
    """Use for tagging a dependency, which should be resolved by name
    and for setting up all client-defined configurations
    """
    def __init__(
        self,
        unique_instance: bool = False,
        default_value: Any = None,
    ):
        self.method = self.Method.BY_NAME
        self.unique_instance = unique_instance
        self.default_value = default_value
