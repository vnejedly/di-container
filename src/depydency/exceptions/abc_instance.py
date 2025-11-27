from typing import Type


class AbcInstanceException(Exception):
    def __init__(self, dependency_type: Type, previous: Exception):
        self.dependency_type = dependency_type
        self.previous = previous
        super().__init__(
            f"Can't create instance of {dependency_type}. "
            f"If it's abstract, provide an implementation via the "
            f"Alias provider or set a default implementation via "
            f"TypeInject. Reason: {previous}"
        )
