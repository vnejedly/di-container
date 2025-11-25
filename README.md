<p align="left">
  <img src="https://raw.githubusercontent.com/vnejedly/depydency/refs/heads/main/docs/logo.png" alt="depydency logo" width="200"/>
</p>

## Dependency Injection (DI) container and Inversion Of Control (IoC) helper library

A lightweight IoC (inversion of control) and DI (dependency-injection) container to register and resolve services by type or by name. I allows recursive autowiring of the whole dependency tree as well as custom configuration of particular dependencies.

---

### Table of contents

1. Installation
2. Concepts
3. Basic usage
4. Container setup & Providers
5. `TypeInject` & `NameInject` annotations
6. Usage example

---

### Installation

```bash
pip install depydency
```

---

### Concepts

- Container: holds various dependency providers.

- Provider: an object that knows how to produce the value/instance for a particular dependency ba type or name.
    - `Value`: always return the given instance/value.
    - `Callback`: call a factory function to produce the instance.
    - `Alias`: map an interface/abstract type to a concrete implementation.
    - `AutoResolve`: FOR INTERNAL USAGE ONLY - (when available) try to construct a type automatically.
---

### Basic usage

The class AbcContainer is to be extended by a child class, which contains the particular container configuration. The method `setup` must be implemented (empty in the case of minimal configuration). In the entrypoint / front controller of your application, just create an intance of this child (inherited from the AbcContainer) class and get the "root service" of your dependency tree, either by get_by_type or get_by_name bethod. You will just get the instance of your class, with whole dependency tree resolved automatically by default, or customized through the container `setup` method.


### Container setup & Providers

In the container `setup` method you can pass so called "providers", which are special classes having responsibility for creating the instance of each of your dependencies. By default with no particular provider configured, the `AutoResolve` provider will be used internally for creating instance of each of your dependencies out of the box. If you want to customize the instantiation of any of your dependencies, you can pass a provider by calling one of the methods `provide_type` or `provine_name`. You can use

- `Value` the most simple, trivial case, where you just create the instance manually and provide it for every dependent object across the dependency tree. This is most useful for the scalar values (like `string`, `int` or `float` constants you want to provide across the application, but avoiding to poison the global scope)
- `Callback` for providing instance by a callable, where you have complete control of the instantiation in the runtime, when the dependency is demanded. The provider callback hass access to the `provider` object itself as well as to the `inject` object cantaining the dependency metadata, which can be used for customizing the instantiation. When you create the instance, you can provide all its dependencies manually, using `provider.get_container().get_by_type(...)`, `provider.get_container().get_by_name(...)`, simply autoresolve them by calling `provider.inject_dependencies(instance)`. In the las possibility, you can also pass a dictionary of instances for dependencies you want to satisfy arbitrary between those, which will be autoresolved.
- `Alias` especially useful, when your dependency is defined by an abstract class or interface and so the container setup must decide, which concrete implementation will be provided for the abc class demanded. This is the core of the IoC (Inversion of Control) concept. Not the dependent class itself, but the app configuration thus decides about the particular dependency implementation. The particular implementation (the target class) can be either autoresolved, or provided by one of the methods above.


### `TypeInject` & `NameInject` annotations

This is the key point of whole the dependency injection. In each of the class from your dependency tree, you have to mark all its dependencies by the special annotation:

```python
class SomeDependencyTreeClass:
    # these dependencies will be resolved by container according the type
    # provided as the first subscription of the Annotaded hint
    dependency_1: Annotated[AnotherDependencyTreeClass, TypeInject()]
    dependency_2: Annotated[SomeDependencyClassInterface, TypeInject()]
    ...

    # this dependency will be resolved by container according the neme of
    # the property ("dependency_5")
    dependency_5: Annotated[str, NameInject()]
    ...

    annotation_or_class_property: SomeType = ...some value...
    ...
```

You can also provide arguments for the `TypeInject` and `NameInject` marker object. The most important is `TypeInject(unique_instance=True)`. By setting it you say, that each time an instance of that dependency is demanded in your dependency tree, a brand new (unique across the application) instance of that class will be created and provided. The default value, however, is `False`, which is wanted for most DI use-cases and thus a sigle one (singleton) instance of that class will be shared across the application and the dependency tree.


### Usage Example

File: `a_package/abc_speaker_interface.py`
```python
from abc import ABC, abstractmethod


class AbcSpeakerInterface(ABC):
    
    @abstractmethod
    def speak(self) -> str:
        pass

```


File: `a_package/speaker_a.py`
```python
from a_package.abc_speaker_interface import AbcSpeakerInterface
from a_package.x_class import XClass
from depydency.inject import TypeInject
from typing import Annotated


class SpeakerA(AbcSpeakerInterface):
    instances_count: int = 0

    x_object: Annotated[XClass, TypeInject()]

    def __init__(self):
        SpeakerA.instances_count += 1
        self.instance_num: int = self.instances_count

    def speak(self) -> str:
        return (
            f"I am instance {self.instance_num} of speaker A "
            f"having also an instance of {self.x_object.get_name()}"
        )
```


File: `a_package/a_class.py`
```python
from a_package.speaker_a import SpeakerA
from a_package.speaker_b import SpeakerB
from a_package.abc_speaker_interface import AbcSpeakerInterface
from depydency.inject import TypeInject, NameInject
from typing import Annotated


class AClass:
    # inject "some" implementation of the AbcSpeakerInterface, which must
    # be specified by an Alias provider in the container setup. Otherwise
    # the injection will not work (the container will not know, what to inject)
    speaker_1: Annotated[AbcSpeakerInterface, TypeInject()]

    # inject the SpeakerB for this dependency, as configured (or not) in the
    # container
    speaker_3: Annotated[SpeakerB, TypeInject()]

    # inject whatever the container has cofigured by a named provider for the
    # dependency name "some_named_dependency". The type provided must match with
    # the type in the annotation (str for this case)
    some_named_dependency: Annotated[str, NameInject(default_value="Hovadina")]

    # a class property, which will be not touched by the container
    some_class_property: str = 'tezt'

    # an "empty" annotation, which will be ignored by the container
    some_annotation: SomeType

    @property
    def info(self) -> str:
        return (
            f"Script name: {self.some_named_dependency}\n"
            f"Class A (instances count = {SpeakerA.instances_count})\n"
            f"Speaker 1: {self.speaker_1.speak()}\n"
            f"Speaker 2: {self.speaker_2.speak()}\n"
            f"Speaker 3: {self.speaker_3.speak()}\n"
        )
```


File: `container.py`
```python
from a_package.abc_speaker_interface import AbcSpeakerInterface
from a_package.speaker_a import SpeakerA
from a_package.speaker_b import SpeakerB
from depydency.abc_container import AbcContainer
from depydency.provider.alias import Alias
from depydency.provider.value import Value
from depydency.provider.callback import Callback
from depydency.provider.abc_creator import AbcCreator
from depydency.inject import Inject


class Container(AbcContainer):
    def setup(self):
        # will provide the SpeakerA implementation for the AbcSpeakerInterface
        # either autoresolved or provided by another provider
        self.provide_type(Alias(AbcSpeakerInterface, SpeakerA))

        # vill provide the instance by the self.create_speaker_a function
        self.provide_type(Callback(SpeakerA, self.create_speaker_a))

        # will simply provide the SpeakerB instance created immediately
        self.provide_type(Value(SpeakerB()))

        # the string type and Value provider in this case is just an example, 
        # you can use any type or class with any type of provider
        self.provide_name("some_named_dependency", Value("Some value of any type."))

    @staticmethod
    def create_speaker_a(provider: AbcCreator, inject: Inject) -> SpeakerA:
        instance = SpeakerA()

        # by calling this, you can inject the dependencies automatically, and
        # optionally provide the selected dependencies as a dictionary manually 
        # as the second argument 
        provider.inject_dependencies(instance, {
            "some_dependency_name": SomeDependencyClacs(...),
            ...
        })

        return instance
```


File: `__main__.py`
```python
from a_package.a_class import AClass
from container import Container


container = Container()
a_class_1 = container.get_by_type(AClass)
a_class_2 = container.get_by_type(AClass)

print(a_class_1.info)
print(a_class_2.info)        

```