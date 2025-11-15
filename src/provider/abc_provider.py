from __future__ import annotations
from typing import Dict
from di_tree.inject import Inject
from di_tree.exceptions.bad_type import BadTypeException
from di_tree.exceptions.not_callable import NotCallableException
from di_tree.provider.abc_provider_interface import AbcProviderInterface
from typing import Any, Type, Callable, TYPE_CHECKING
from abc import ABC

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

        for (dep_name, dep_type) in instance_type.__annotations__.items():
            if isinstance(inject := getattr(instance_type, dep_name, None), Inject):
                dependency_instance = self._container.get_dependency(inject, dep_type, dep_name)
                setattr(instance, dep_name, dependencies.get(dep_name, dependency_instance))

    def _create_instance(self) -> Any:
        instance = self._creator(self)
        type_provided = type(instance)
        if type_provided != self._dependency_type:
            raise BadTypeException(self._dependency_type, type_provided)

        return instance

