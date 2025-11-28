from abc import ABC, abstractmethod
from typing import Dict, Type, Any
from depydency.abc_locator_interface import AbcLocatorInterface
from depydency.provider.abc_provider import AbcProvider
from depydency.provider.auto_resolve import AutoResolve
from depydency.exceptions.bad_name import BadNameException
from depydency.exceptions.abc_instance import AbcInstanceException
from depydency.inject import Inject, TypeInject, NameInject


class AbcContainer(AbcLocatorInterface, ABC):
    """The core DI container class. Holds all dependencies configuration and
    is responsible for the resursive resolution of the whole dependency tree.
    Must be extended to work properly and for the (optional) configuration.
    """
    _providers_type: Dict[str, AbcProvider]
    _providers_name: Dict[str, AbcProvider]

    def __init__(self):
        self._providers_type = {}
        self._providers_name = {}
        self.setup()

    @abstractmethod
    def setup(self):
        """Setup dependences in the extension class"""

    def provide_type(self, provider: AbcProvider):
        """Setup provider to provide dependency by type"""
        type_repr = self._get_type_repr(provider.dependency_type)
        self._providers_type[type_repr] = provider
        provider.set_container(self)

    def provide_name(self, name: str, provider: AbcProvider):
        """Setup provider to provide dependency by name"""
        self._providers_name[name] = provider
        provider.set_container(self)

    def get_by_type[DependencyType](
        self, dependency_type: Type[DependencyType],
        unique_instance: bool = False,
        default_implementation: Type | None = None,
    ) -> DependencyType:
        """Get the root dependency by type inside your program entry-point"""
        inject = TypeInject(unique_instance, default_implementation)
        inject.set_dependency_id(dependency_type=dependency_type)
        return self.get_dependency(inject)
        
    def get_by_name(
        self, dependency_name: str,
        unique_instance: bool = False,
        default_value: Any = None
    ) -> Any:
        """Get the root dependency by name inside your program entry-point"""
        inject = NameInject(unique_instance, default_value)
        inject.set_dependency_id(dependency_name=dependency_name)
        return self.get_dependency(inject)

    def get_dependency(self, inject: Inject) -> Any:
        """FOR INTERNAL USAGE ONLY. For root dependency resolution, use
        the get_by_type or get_by_name method.
        """
        match inject.method:
            case Inject.Method.BY_TYPE:
                type_repr = self._get_type_repr(inject.dependency_type)
                if type_repr not in self._providers_type.keys():
                    self.provide_type(AutoResolve(inject.dependency_type))
                try:
                    return self._providers_type.get(type_repr).provide(inject)
                except TypeError as exception:
                    if inject.default_implementation is None:
                        raise AbcInstanceException(inject.dependency_type, exception)
                    default_repr = self._get_type_repr(inject.default_implementation)
                    if default_repr not in self._providers_type.keys():
                        self.provide_type(AutoResolve(inject.default_implementation))
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
        """Generate a unique string representation of the type"""
        return f"{dependency_type.__module__}.{dependency_type.__name__}"
