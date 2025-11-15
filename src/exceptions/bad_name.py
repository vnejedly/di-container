class BadNameException(Exception):

    def __init__(self, dependency_name: str):
        self.dependency_name = dependency_name
        super().__init__(
            f"Named dependency '{dependency_name}' does not exist"
        )
