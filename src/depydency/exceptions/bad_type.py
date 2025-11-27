from typing import Type


class BadTypeException(Exception):
    def __init__(self, type_expected: Type, type_provided: Type):
        self.type_expected = type_expected
        self.type_provided = type_provided
        super().__init__(
            f"Expected class {type_expected}, got {type_provided} from provider"
        )
