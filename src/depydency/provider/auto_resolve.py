from typing import Type, Any
from depydency.provider.abc_creator import AbcCreator
from depydency.inject import Inject
import importlib


class AutoResolve(AbcCreator):
    """FOR INTERNAL USAGE ONLY.
    Provides the requested dependency by its type automatically
    """
    def __init__(self, dependency_type: Type):
        self._dependency_type = dependency_type
        self._instance = None

    def _creator(self, inject: Inject) -> Any:
        module = importlib.import_module(self.dependency_type.__module__)
        dependency_type = getattr(module, self.dependency_type.__name__)
        
        instance = dependency_type()
        self.inject_dependencies(instance)
        
        return instance
