import requests

class DownloadError(Exception):
    """
    Exception for download errors.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__("[!] Error while downloading")


class UrlParserError(Exception):
    """
    Exception for url parsing errors.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__("[!] Error while parsing url")


class SaveError(Exception):
    """
    Exception for save errors.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__("[!] Error while saving")