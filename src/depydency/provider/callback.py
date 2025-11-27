from depydency.inject import Inject
from depydency.provider.abc_creator import AbcCreator
from typing import Type, Any, Callable

CreatorCallable = Callable[[AbcCreator, Inject], Any]


class Callback(AbcCreator):
    """Provides the dependency using a custom callable"""
    def __init__(self, dependency_type: Type, creator_callable: CreatorCallable):
        assert callable(creator_callable), "Pass a callable"

        self._dependency_type = dependency_type
        self._creator_callable = creator_callable
        self._instance = None

    def _creator(self, inject: Inject) -> Any:
        return self._creator_callable(self, inject)
