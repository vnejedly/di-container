from abc import ABC, abstractmethod
from typing import Type
from di_tree.inject import TypeInject


class AbcLocatorInterface(ABC):

    @abstractmethod
    def get_by_type[DependencyType](
        self, dependency_type: Type[DependencyType], 
        inject_params: TypeInject = TypeInject(),
    ) -> DependencyType:
        pass
