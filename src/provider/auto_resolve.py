from typing import Type, Any, Dict
from di_tree.provider.explicit_callable import ExplicitCallable
from di_tree.inject import TypeInject, NameInject
import importlib


class AutoResolve[DependencyType](ExplicitCallable):

    def __init__(self, dependency_type: Type[DependencyType]):
        super().__init__(dependency_type, self._creator)

    def _creator(self) -> DependencyType:
        module = importlib.import_module(self._dependency_type.__module__)
        type_reference = getattr(module, self._dependency_type.__name__)

        instance = type_reference()
        self.inject_dependencies(instance)

        return instance

    def inject_dependencies(self, instance: Any, dependencies: Dict[str, Any] = None):
        if dependencies is None:
            dependencies = {}

        instance_type = type(instance)

        for (dep_name, dep_type) in instance_type.__annotations__.items():
            inject_params = getattr(instance_type, dep_name)
            if isinstance(inject_params, TypeInject):
                dependency_instance = self._container.get_by_type(dep_type, inject_params)
            elif isinstance(inject_params, NameInject):
                dependency_instance = self._container.get_by_name(dep_name, inject_params)
            else:
                raise ValueError(f"Unexpected type {inject_params}")
            
            setattr(instance, dep_name, dependencies.get(dep_name, dependency_instance))
