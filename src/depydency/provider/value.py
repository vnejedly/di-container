from typing import Any, Type, TYPE_CHECKING
from depydency.provider.abc_provider import AbcProvider
from depydency.inject import Inject


class Value(AbcProvider):
    """Provides the dependency instance passed explicitly in constructor."""
    def __init__(self, value: Any):
        self._value = value

    @property
    def dependency_type(self) -> Type:
        return type(self._value)

    def provide(self, inject: Inject) -> Any:
        assert inject.unique_instance == False, "Can only inject the actual value"
        return self._value

