import random
import time
from functools import lru_cache
from threading import Lock


# Без кешу
def range_sum_no_cache(array, L, R):
    """
    Обчислює суму елементів у масиві на відрізку від індексу L до R включно.
    Ця функція не використовує кешування і кожного разу обчислює результат заново.

    Параметри:
        array (list[int]): Масив цілих чисел.
        L (int): Початковий індекс відрізка (включно).
        R (int): Кінцевий індекс відрізка (включно).

    Повертає:
        int: Сума елементів на відрізку від L до R включно.
    """
    return sum(array[L:R+1])


def update_no_cache(array, index, value):
    """
    Оновлює значення елемента масиву за вказаним індексом без використання кешу.

    Параметри:
        array (list[int]): Масив цілих чисел.
        index (int): Індекс, який потрібно оновити.
        value (int): Нове значення для оновлення.

    Генерує:
        IndexError: Якщо індекс виходить за межі масиву.
    """
    if not 0 <= index < len(array):
        raise IndexError("Індекс виходить за межі масиву")
    array[index] = value


# З кешем
LRU_CACHE_SIZE = 1000
array_reference = []  # Глобальне посилання для кешування
array_lock = Lock()  # Блокування для потокобезпеки


@lru_cache(maxsize=LRU_CACHE_SIZE)
def cached_range_sum(array_id, L, R):
    with array_lock:
        return sum(array_reference[L:R+1])


def range_sum_with_cache(array, L, R):
    """
    Обчислює суму елементів у масиві на відрізку від індексу L до R включно з використанням LRU-кешу.

    Параметри:
        array (list[int]): Масив цілих чисел.
        L (int): Початковий індекс відрізка (включно).
        R (int): Кінцевий індекс відрізка (включно).

    Повертає:
        int: Сума елементів на відрізку від L до R включно.
    """
    global array_reference
    with array_lock:
        array_reference = array
    return cached_range_sum(id(array), L, R)


def update_with_cache(array, index, value):
    """
    Оновлює значення елемента масиву за вказаним індексом і очищає кеш.

    Параметри:
        array (list[int]): Масив цілих чисел.
        index (int): Індекс, який потрібно оновити.
        value (int): Нове значення для оновлення.

    Генерує:
        IndexError: Якщо індекс виходить за межі масиву.
    """
    global array_reference
    if not 0 <= index < len(array):
        raise IndexError("Індекс виходить за межі масиву")
    with array_lock:
        array[index] = value
        # Очищення кешу для забезпечення коректності після оновлення
        cached_range_sum.cache_clear()


# Генерація тестових даних
N = 100_000
Q = 50_000
array = [random.randint(1, 100) for _ in range(N)]
queries = []

for _ in range(Q):
    if random.choice([True, False]):
        L = random.randint(0, N - 1)
        R = random.randint(L, N - 1)
        queries.append(('Range', L, R))
    else:
        index = random.randint(0, N - 1)
        value = random.randint(1, 100)
        queries.append(('Update', index, value))

# Виконання без кешу
start_time_no_cache = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_no_cache(array, query[1], query[2])
    elif query[0] == 'Update':
        update_no_cache(array, query[1], query[2])
end_time_no_cache = time.time()

# Виконання з кешем
start_time_with_cache = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_with_cache(array, query[1], query[2])
    elif query[0] == 'Update':
        update_with_cache(array, query[1], query[2])
end_time_with_cache = time.time()

# Результати
execution_time_no_cache = end_time_no_cache - start_time_no_cache
execution_time_with_cache = end_time_with_cache - start_time_with_cache

print(f"Час виконання без кешування: {execution_time_no_cache:.2f} секунд")
print(f"Час виконання з LRU-кешем: {execution_time_with_cache:.2f} секунд")

if execution_time_with_cache < execution_time_no_cache:
    print("Використання LRU-кешу покращує продуктивність.")
else:
    print("LRU-кеш не забезпечив переваг у продуктивності.")
