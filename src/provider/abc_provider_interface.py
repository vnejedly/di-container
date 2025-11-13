from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Type, TYPE_CHECKING
from di_tree.inject import TypeInject

if TYPE_CHECKING:
    from di_tree.abc_container import AbcContainer


class AbcProviderInterface(ABC):

    @abstractmethod
    def provide(self, inject_params: TypeInject = TypeInject()) -> Any:
        pass

    @abstractmethod
    def get_dependency_type(self) -> Type:
        pass

    @abstractmethod
    def set_container(self, container: AbcContainer):
        pass
