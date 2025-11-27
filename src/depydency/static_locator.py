from typing import Type, Any
from depydency.abc_locator_interface import AbcLocatorInterface


class StaticLocator:
    """Use as a workaround, when you need to create a safe DI space inside
    an old-fashioned static-bloated project or framework."""
    locator: AbcLocatorInterface

    @classmethod
    def get_by_type[DependencyType](
        cls, dependency_type: Type[DependencyType],
        unique_instance: bool = False,
        default_implementation: Type | None = None,
    ) -> DependencyType:
        """Get the root dependency by type inside your script entry-point"""
        return cls.locator.get_by_type(
            dependency_type, unique_instance, default_implementation
        )
        
    @classmethod
    def get_by_name(
        cls, dependency_name: str,
        unique_instance: bool = False,
        default_value: Any = None,
    ) -> Any:
        """Get the root dependency by name inside your script entry-point"""
        return cls.locator.get_by_name(dependency_name, unique_instance, default_value)
