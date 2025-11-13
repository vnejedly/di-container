from typing import Type, Any


class TypeInject:
    def __init__(
        self, 
        unique_instance: bool = False,
        default_implementation: Type | None = None,
    ):
        self.unique_instance = unique_instance
        self.default_implementation = default_implementation


class NameInject:
    def __init__(
        self,
        default_value: Any = None,
    ):
        self.default_value = default_value
