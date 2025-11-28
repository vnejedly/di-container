from typing import Any, Type
from depydency.provider.abc_provider import AbcProvider
from depydency.inject import Inject


class Alias(AbcProvider):
    """Fulfills the IoC (Inversion of Control) principle.
    Defines a target type, which will be provided, when the alias type 
    is requested. Intended for configuring particular implementations
    for abstract dependencies requested across the dependency tree.
    """
    _alias_type: Type
    _target_type: Type

    def __init__(self, alias_type: Type, target_type: Type):
        self._alias_type = alias_type
        self._target_type = target_type

    def provide(self, inject: Inject) -> Any:
        inject.set_dependency_id(dependency_type=self._target_type)
        return self._container.get_dependency(inject)

    def get_dependency_type(self) -> Type:
        return self._alias_type
