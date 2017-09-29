class InvalidInput(Exception):
    """
    This error will indicate the input violates the rules that set up in the package.
    Detailed information will be provided for the invalid input.
    """
    pass


class FileNotFound(Exception):
    """
    This error will indicate the input some critical files can not be found.
    Detailed information will be provided for the invalid input.
    """
    pass
