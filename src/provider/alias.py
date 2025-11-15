from __future__ import annotations
from typing import Any, Type, TYPE_CHECKING
from di_tree.provider.abc_provider_interface import AbcProviderInterface
from di_tree.inject import Inject

if TYPE_CHECKING:
    from di_tree.abc_container import AbcContainer


class Alias(AbcProviderInterface):

    _container: AbcContainer
    _alias_class: Type
    _target_class: Type

    def __init__(self, alias_type: Type, target_type: Type):
        self._alias_class = alias_type
        self._target_class = target_type

    def provide(self, inject: Inject) -> Any:
        return self._container.get_dependency(
            inject=inject, dependency_type=self._target_class,
        )

    def get_dependency_type(self) -> Type:
        return self._alias_class

    def set_container(self, container: AbcContainer):
        self._container = container
