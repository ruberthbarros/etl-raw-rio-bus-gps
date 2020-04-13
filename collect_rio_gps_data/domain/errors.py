"""errors.py - project related errors module"""


class EmptyResponseError(Exception):
    def __init__(self, request):
        message = f"The {request} returned an empty response."
        super().__init__(message)
