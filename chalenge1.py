def check_input_arguments(args, types):
    for arg in args:
        if not isinstance(arg, types):
            print('Invalid input arguments, expected {}!'.format(', '.join(str(type) for type in types)))
            return False
    return True
        

def type_check(val):
    """Check the types of the input and output of a function."""

    def wrapper(*types):
        def decorator(func):
            def check_types(*args, **kwargs):
                if isinstance(val, str):
                    if val == 'in':
                        check_input_arguments(args,types)

                    res = func(*args, **kwargs)

                    if val == 'out':
                        if not isinstance(res, types):
                            print('Invalid output value, expected {}!'.format(', '.join(str(type) for type in types)))
                
                return res
            return check_types
        return decorator
    return wrapper