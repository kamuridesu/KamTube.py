class UnknownFileError(FileNotFoundError):
    def __init__(self, message: str="An error occured while getting the files and the reason is not clear! Check the logs for more information") -> None:
        super().__init__(message)
