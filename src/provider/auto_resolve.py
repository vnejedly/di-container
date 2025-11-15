from typing import Type, Any
from di_tree.provider.explicit_callable import ExplicitCallable
from di_tree.provider.abc_provider import AbcProvider
import importlib


class AutoResolve(ExplicitCallable):

    def __init__(self, dependency_type: Type):
        def creator(_) -> Any:
            module = importlib.import_module(self._dependency_type.__module__)
            type_reference = getattr(module, self._dependency_type.__name__)

            instance = type_reference()
            self.inject_dependencies(instance)

            return instance

        super().__init__(dependency_type, creator)
