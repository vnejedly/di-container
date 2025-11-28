from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Type, TYPE_CHECKING
from depydency.inject import Inject

if TYPE_CHECKING:
    from depydency.abc_container import AbcContainer


class AbcProvider(ABC):
    """An abstraction for all dependency providers."""
    container: AbcContainer

    @property
    @abstractmethod
    def dependency_type(self) -> Type:
        """Return the type of the dependency to be provided"""

    @abstractmethod
    def provide(self, inject: Inject) -> Any:
        """Provide an instance of the dependency."""

    def set_container(self, container: AbcContainer):
        """Seter for the container."""
        self.container = container
