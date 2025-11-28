from typing import Dict
from depydency.inject import Inject
from depydency.exceptions.bad_type import BadTypeException
from depydency.provider.abc_provider import AbcProvider
from abc import ABC, abstractmethod

from typing import Any, Type, Annotated, get_type_hints, get_origin, get_args


class AbcCreator(AbcProvider, ABC):
    """An abstraction for all providers, which use the creator method for
    creation the dpendency instance.
    """
    _dependency_type: Type
    _instance: Any

    def get_dependency_type(self) -> Type:
        return self._dependency_type

    def provide(self, inject: Inject) -> Any:
        if inject.unique_instance:
            return self._create_instance(inject)
        
        if self._instance is None:
            self._instance = self._create_instance(inject)

        return self._instance

    def inject_dependencies(self, instance: Any, dependencies: Dict[str, Any] = {}):
        """Inject dependencies to the client object, which has been already created.
        Pass a dependencies dictionary, if you want to provide some of them manually.
        """
        instance_type = type(instance)
        annotations = get_type_hints(instance_type, include_extras=True)
        
        for dependency_name, annotation in annotations.items():
            if get_origin(annotation) == Annotated:
                dependency_type, inject = get_args(annotation)
                if (isinstance(dependency_type, Type) and isinstance(inject, Inject)):
                    inject.set_dependency_id(dependency_type, dependency_name)
                    dependency_instance = dependencies.get(dependency_name)
                    
                    if not dependency_instance:
                        dependency_instance = self._container.get_dependency(inject)
                    elif not isinstance(dependency_instance, inject.dependency_type):
                        raise BadTypeException(
                            inject.dependency_type, type(dependency_instance)
                        )
                    setattr(instance, dependency_name, dependency_instance)

    def _create_instance(self, inject: Inject) -> Any:
        """Create new instance of the dependency based on inject configuration."""
        instance = self._creator(inject)
        type_provided = type(instance)
        if type_provided != self._dependency_type:
            raise BadTypeException(self._dependency_type, type_provided)

        return instance

    @abstractmethod
    def _creator(self, inject: Inject) -> Any:
        """The particular instance method creation defined by the extension class"""
        pass
