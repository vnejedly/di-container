from abc import ABC, abstractmethod
from typing import Type, Any


class AbcLocatorInterface(ABC):
    """Defines an interface for a general dependency locator"""

    @abstractmethod
    def get_by_type[DependencyType](
        self, dependency_type: Type[DependencyType], 
        unique_instance: bool = False,
        default_implementation: Type | None = None,
    ) -> DependencyType:
        """Get the root dependency by type inside your script entry-point"""
        
    @abstractmethod
    def get_by_name(
        self, dependency_name: str, 
        unique_instance: bool = False,
        default_value: Any = None,
    ) -> Any:
        """Get the root dependency by name inside your script entry-point"""
