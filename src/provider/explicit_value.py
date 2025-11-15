from __future__ import annotations
from typing import Any, Type, TYPE_CHECKING
from di_tree.provider.abc_provider_interface import AbcProviderInterface
from di_tree.inject import Inject

if TYPE_CHECKING:
    from di_tree.abc_container import AbcContainer


class ExplicitValue(AbcProviderInterface):
    _container: AbcContainer

    def __init__(self, value: Any):
        self._value = value

    def provide(self, inject: Inject) -> Any:
        return self._value

    def get_dependency_type(self) -> Type:
        return type(self._value)
    
    def set_container(self, container: AbcContainer):
        self._container = container
