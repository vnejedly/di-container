from abc import ABC, abstractmethod
from typing import Type, Any


class AbcLocatorInterface(ABC):

    @abstractmethod
    def get_by_type[DependencyType](
        self, dependency_type: Type[DependencyType], 
        unique_instance: bool = False,
        default_implementation: Type | None = None,
    ) -> DependencyType:
        pass
        
    @abstractmethod
    def get_by_name(
        self, dependency_name: str, 
        default_value: Any = None,
    ) -> Any:
        pass
