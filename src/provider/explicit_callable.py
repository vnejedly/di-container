from typing import Any, Callable, Type
from di_tree.provider.abc_provider import AbcProvider
from di_tree.inject import Inject


class ExplicitCallable(AbcProvider):

    _instance: Any

    def __init__(self, dependency_type: Type, creator: Callable):
        super().__init__(dependency_type, creator)
        self._instance = None

    def provide(self, inject: Inject) -> Any:
        if inject.unique_instance:
            return self._create_instance()

        if self._instance is None:
            self._instance = self._create_instance()

        return self._instance
