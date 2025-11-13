from typing import Type
from di_tree.abc_locator_interface import AbcLocatorInterface
from di_tree.inject import TypeInject


class StaticLocator:

    locator: AbcLocatorInterface

    @classmethod
    def get_by_type[DependencyType](
        cls, dependency_type: Type[DependencyType], 
        inject_params: TypeInject = TypeInject()
    ) -> DependencyType:
        return cls.locator.get_by_type(dependency_type, inject_params)
