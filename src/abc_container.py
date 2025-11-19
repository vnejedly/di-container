from abc import ABC, abstractmethod
from typing import Dict, Type, Any
from di_tree.abc_locator_interface import AbcLocatorInterface
from di_tree.provider.abc_provider_interface import AbcProviderInterface
from di_tree.provider.auto_resolve import AutoResolve
from di_tree.exceptions.bad_name import BadNameException
from di_tree.inject import Inject, TypeInject, NameInject


class AbcContainer(AbcLocatorInterface, ABC):

    _providers_type: Dict[str, AbcProviderInterface]
    _providers_name: Dict[str, AbcProviderInterface]

    def __init__(self):
        self._providers_type = {}
        self._providers_name = {}
        self.setup()

    @abstractmethod
    def setup(self):
        """Setup dependences in implementation"""

    def provider(self, provider: AbcProviderInterface):
        type_repr = self._get_type_repr(provider.get_dependency_type())
        self._providers_type[type_repr] = provider
        provider.set_container(self)

    def named_provider(self, name: str, provider: AbcProviderInterface):
        self._providers_name[name] = provider

    def get_by_type[DependencyType](
        self, dependency_type: Type[DependencyType],
        unique_instance: bool = False,
        default_implementation: Type | None = None,
    ) -> DependencyType:
        inject = TypeInject(unique_instance, default_implementation)
        inject.set_dependency_id(dependency_type=dependency_type)
        return self.get_dependency(inject)
        
    def get_by_name(
        self, dependency_name: str,
        unique_instance: bool = False,
        default_value: Any = None
    ) -> Any:
        inject = NameInject(unique_instance, default_value)
        NameInject.set_dependency_id(dependency_name=dependency_name)
        return self.get_dependency(inject)

    def get_dependency(self, inject: Inject) -> Any:
        match inject.method:
            case Inject.Method.BY_TYPE:
                type_repr = self._get_type_repr(inject.dependency_type)
                if type_repr not in self._providers_type.keys():
                    self.provider(AutoResolve(inject.dependency_type))
                try:
                    return self._providers_type.get(type_repr).provide(inject)
                except TypeError:
                    default_implementation = inject.default_implementation
                    if default_implementation is None:
                        raise
                    default_repr = self._get_type_repr(default_implementation)
                    if default_repr not in self._providers_type.keys():
                        self.provider(AutoResolve(default_implementation))
                    return self._providers_type.get(default_repr).provide(inject)
            case Inject.Method.BY_NAME:
                if inject.dependency_name not in self._providers_name.keys():
                    if inject.default_value is not None:
                        return inject.default_value
                    raise BadNameException(inject.dependency_name)
                return self._providers_name.get(inject.dependency_name).provide(inject)
            
        raise ValueError(f"Unexpected inject method {inject.method}")

    @staticmethod
    def _get_type_repr(dependency_type: Type) -> str:
        return f"{dependency_type.__module__}.{dependency_type.__name__}"
