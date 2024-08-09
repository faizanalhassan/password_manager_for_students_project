import time

def factorial_memorize_decrotor(fn):
    memory = {}
    def wrapper(n):
        if n in memory:
            return memory[n]
        output = fn(n)
        memory[n] = output
        return output
    return wrapper

def factorial_time_calculate(fn):
    def my_modified_fn(n):
        start_time = time.time()
        result = fn(n)
        end_time = time.time()
        print(f"Total time spent to execute with param {n}: {(end_time - start_time)*1000} ms")
        return result
    return my_modified_fn

@factorial_time_calculate
@factorial_memorize_decrotor
def factorial_iterative(n):
    if n < 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        time.sleep(0.01)
        result *= i
    return result

# factorial_iterative = factorial_memorize_decrotor(factorial_iterative)
# Example usage:
print(factorial_iterative(10))  # Output: 120
print(factorial_iterative(10))  # Output: 120
print(factorial_iterative(12))  # Output: 120
print(factorial_iterative(12))  # Output: 120
