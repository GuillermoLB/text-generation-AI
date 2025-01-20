from .codes import Errors, Warnings


class CustomException(Exception):
    def __init__(self, error: Errors | Warnings, code: int):
        self.error = error
        self.code = code

    def __str__(self):
        return self.error


class ModelException(CustomException):

    """
    All Model' related exceptions with specific error codes
    """


class TextGenerationException(CustomException):

    """
    All Text_generation' related exceptions with specific error codes
    """


class UserException(CustomException):

    """
    All User' related exceptions with specific error codes
    """


class AuthenticationException(CustomException):

    """
    All User' related exceptions with specific error codes
    """
