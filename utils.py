def validate_expression(expression: bool, exception: Exception):
    """
    This function is intended to validate a boolean expression and to raise an
    exception if it is not true

    Parameters
    ----------
    expression: bool
        The expression to validate
    exception: Exception
        The exception that will be thrown if the expression is false
    """
    if not expression:
        raise exception