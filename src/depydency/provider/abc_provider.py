from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Type, TYPE_CHECKING
from depydency.inject import Inject

if TYPE_CHECKING:
    from depydency.abc_container import AbcContainer


class AbcProvider(ABC):
    """An abstraction for all dependency providers."""
    _container: AbcContainer

    @abstractmethod
    def provide(self, inject: Inject) -> Any:
        """Provide an instance of the dependency."""

    @abstractmethod
    def get_dependency_type(self) -> Type:
        """Returns the type of the dependency defined by the provider"""

    def get_container(self) -> AbcContainer:
        """Getter for the container."""
        return self._container

    def set_container(self, container: AbcContainer):
        """Seter for the container."""
        self._container = container
