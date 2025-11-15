from typing import Type, Any
from di_tree.abc_locator_interface import AbcLocatorInterface
from di_tree.inject import Inject


class StaticLocator:

    locator: AbcLocatorInterface

    @classmethod
    def get_by_type[DependencyType](
        cls, dependency_type: Type[DependencyType], 
        unique_instance: bool = False,
        default_implementation: Type | None = None,
    ) -> DependencyType:
        return cls.locator.get_by_type(dependency_type, unique_instance, default_implementation)
        
    @classmethod
    def get_by_name(
        cls, dependency_name: str, 
        default_value: Any = None,
    ) -> Any:
        return cls.locator.get_by_name(dependency_name, default_value)
