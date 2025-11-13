from abc import ABC, abstractmethod
from typing import Dict, Type, Any
from di_tree.abc_locator_interface import AbcLocatorInterface
from di_tree.provider.abc_provider_interface import AbcProviderInterface
from di_tree.provider.auto_resolve import AutoResolve
from di_tree.exceptions.abc_instance import AbcInstanceException
from di_tree.exceptions.bad_name import BadNameException
from di_tree.inject import TypeInject, NameInject


class AbcContainer(AbcLocatorInterface, ABC):

    _providers_repr: Dict[str, AbcProviderInterface]
    _providers_name: Dict[str, AbcProviderInterface]

    def __init__(self):
        self._providers_repr = {}
        self._providers_name = {}
        self.setup()

    @abstractmethod
    def setup(self):
        """Setup dependences in implementation"""

    def set_provider(self, provider: AbcProviderInterface):
        dependency_repr = self._get_dependency_repr(provider.get_dependency_type())
        self._providers_repr[dependency_repr] = provider
        provider.set_container(self)

    def set_named_provider(self, name: str, provider: AbcProviderInterface):
        self._providers_name[name] = provider

    def get_by_type[DependencyType](
        self, dependency_type: Type[DependencyType], 
        inject_params: TypeInject = TypeInject(),
    ) -> DependencyType:
        dependency_repr = self._get_dependency_repr(dependency_type)
        if dependency_repr not in self._providers_repr.keys():
            self.set_provider(AutoResolve(dependency_type))

        try:
            return self._providers_repr.get(dependency_repr).provide(inject_params)
        except TypeError:
            default_implementation = inject_params.default_implementation
            if default_implementation is None:
                raise AbcInstanceException(dependency_type)
            
            default_repr = self._get_dependency_repr(default_implementation)
            if default_repr not in self._providers_repr.keys():
                self.set_provider(AutoResolve(default_implementation))
            
            return self._providers_repr.get(default_repr).provide(inject_params)
        
    def get_by_name(
        self, dependency_name: str, 
        inject_params: NameInject = NameInject(),
    ) -> Any:
        if dependency_name not in self._providers_name.keys():
            if inject_params.default_value is not None:
                return inject_params.default_value
            raise BadNameException(dependency_name)
        return self._providers_name.get(dependency_name).provide()

    @staticmethod
    def _get_dependency_repr(service_class: Type) -> str:
        return f"{service_class.__module__}.{service_class.__name__}"
