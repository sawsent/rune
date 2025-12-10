class NotFoundError(RuntimeError):
    def __init__(self, message: str = "Not found"):
        super().__init__(message)
        self.message = message

