from __future__ import annotations
from typing import Dict
from di_tree.inject import Inject
from di_tree.exceptions.bad_type import BadTypeException
from di_tree.exceptions.not_callable import NotCallableException
from di_tree.provider.abc_provider_interface import AbcProviderInterface
from abc import ABC

from typing import (
    Any, Type, Callable, Annotated, 
    get_type_hints, get_origin, get_args, TYPE_CHECKING
)

if TYPE_CHECKING:
    from di_tree.abc_container import AbcContainer


class AbcProvider(AbcProviderInterface, ABC):

    _container: AbcContainer
    _dependency_type: Type
    _creator: Callable

    def __init__(self, dependency_type: Type, creator: Callable):
        if not callable(creator):
            raise NotCallableException(dependency_type)

        self._dependency_type = dependency_type
        self._creator = creator

    def get_dependency_type(self) -> Type:
        return self._dependency_type

    def set_container(self, container: AbcContainer):
        self._container = container

    def inject_dependencies(self, instance: Any, dependencies: Dict[str, Any] = None):
        if dependencies is None:
            dependencies = {}

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

                    setattr(instance, dependency_name, dependency_instance)

    def _create_instance(self, inject: Inject) -> Any:
        instance = self._creator(self, inject)
        type_provided = type(instance)
        if type_provided != self._dependency_type:
            raise BadTypeException(self._dependency_type, type_provided)

        return instance
