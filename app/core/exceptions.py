class DataBaseConnectionError(Exception):
    """
    Exception raised when the database connection is not alive.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
