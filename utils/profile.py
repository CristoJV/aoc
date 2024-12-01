import time
from functools import wraps

def timeit(repeats = 10):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            total_time = 0
            for i in range(repeats):
                start_time = time.time()
                result = func(*args, **kwargs)
                total_time += (time.time()-start_time)
            average_time = total_time /repeats
            print(f"Function '{func.__name__} executed {repeats} times. Average time: {average_time:.6f} seconds.")
            return result
        return wrapper
    return decorator