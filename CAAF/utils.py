import time


def timefunc(f):
    '''
    Decorator to time how long a function call takes

    :param f: Function to time
    :return: Decorated function which outputs the duration of the function call
    '''
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 'time')
        return result

    return f_timer
