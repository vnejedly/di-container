from typing import Any, Type
from depydency.provider.abc_provider import AbcProvider
from depydency.inject import Inject


class Alias(AbcProvider):
    """Define an alias type, which should be resolved when a particular
    type is requested. Especially suitable for configuring a particular
    implementation for an abstraction demanded by a client object.
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
