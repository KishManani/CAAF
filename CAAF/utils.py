import time


def timefunc(f):
    """

    Parameters
    ----------
    f : function
        Function to time

    Returns
    -------
    f_timed : function
        Decorated function which now prints the time it took to execute.

    """

    def f_timed(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 'time')
        return result

    return f_timed