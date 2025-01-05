import timeit
from functools import lru_cache
import matplotlib.pyplot as plt


# Реалізація обчислення чисел Фібоначчі за допомогою LRU Cache
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    # Базові випадки
    if n <= 1:
        return n
    # Рекурсивне обчислення
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


# Вузол для Splay Tree
class SplayTreeNode:
    def __init__(self, key, value):
        self.key = key  # Ключ вузла (номер числа Фібоначчі)
        self.value = value  # Значення вузла (результат)
        self.left = None  # Лівий дочірній вузол
        self.right = None  # Правий дочірній вузол


# Реалізація Splay Tree
class SplayTree:
    def __init__(self):
        self.root = None  # Корінь дерева

    # Основний алгоритм Splay для переміщення вузла до кореня
    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        # Ключ знаходиться у лівому піддереві
        if key < root.key:
            if root.left is None:
                return root

            # Zig-Zig (лівий-лівий випадок)
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            # Zig-Zag (лівий-правий випадок)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)

            return root if root.left is None else self._rotate_right(root)

        # Ключ знаходиться у правому піддереві
        else:
            if root.right is None:
                return root

            # Zag-Zag (правий-правий випадок)
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            # Zag-Zig (правий-лівий випадок)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)

            return root if root.right is None else self._rotate_left(root)

    # Ліва ротація
    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    # Права ротація
    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    # Вставка нового вузла у дерево
    def insert(self, key, value):
        if self.root is None:
            self.root = SplayTreeNode(key, value)
            return

        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return

        new_node = SplayTreeNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    # Пошук значення у дереві
    def find(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None


# Обчислення чисел Фібоначчі з використанням Splay Tree
def fibonacci_splay(n, tree):
    # Базові випадки
    if n <= 1:
        return n

    # Пошук у дереві
    if (result := tree.find(n)) is not None:
        return result

    # Обчислення та вставка у дерево
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


# Тестування та порівняння
n_values = range(0, 1000, 50)  # Набір значень n
lru_times = []  # Час для LRU Cache
splay_times = []  # Час для Splay Tree


for n in n_values:
    # Час виконання для LRU Cache
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10) / 10
    lru_times.append(lru_time)

    # Час виконання для Splay Tree
    tree = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=10) / 10
    splay_times.append(splay_time)


# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, label="LRU Cache", marker="o")
plt.plot(n_values, splay_times, label="Splay Tree", marker="x")
plt.xlabel("Число Фібоначчі (n)")
plt.ylabel("Середній час виконання (сек)")
plt.title("Порівняння продуктивності обчислення чисел Фібоначчі для LRU Cache та Splay Tree")
plt.legend()
plt.grid(True)
plt.show()


# Виведення результатів у вигляді таблиці
print(f"{'n':<10}{'LRU Cache час (с)':<20}{'Splay Tree час (с)'}")
print("-" * 50)
for n, lru_time, splay_time in zip(n_values, lru_times, splay_times):
    print(f"{n:<10}{lru_time:<20.10f}{splay_time:<20.10f}")