from typing import Type


class AbcInstanceException(Exception):

    def __init__(self, abc_type: Type):
        self.abc_type = abc_type

        super().__init__(
            f"Trying to instantiate {self.abc_type.__name__}, "
            f"default implementation missing"
        )
