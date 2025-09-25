# Análisis de performance universal
import time

def profile_func(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Duración: {end - start}s")
        return result
    return wrapper
