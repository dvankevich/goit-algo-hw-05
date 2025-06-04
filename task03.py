'''
Порівняйте ефективність алгоритмів пошуку підрядка: Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа 
на основі двох текстових файлів (стаття 1, стаття 2). Використовуючи timeit, треба виміряти час виконання 
кожного алгоритму для двох видів підрядків: одного, що дійсно існує в тексті, та іншого — вигаданого 
(вибір підрядків за вашим бажанням). На основі отриманих даних визначте найшвидший алгоритм для кожного тексту 
окремо та в цілому.
'''
import timeit

def build_shift_table(pattern):
  """Створити таблицю зсувів для алгоритму Боєра-Мура."""
  table = {}
  length = len(pattern)
  # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
  for index, char in enumerate(pattern[:-1]):
    table[char] = length - index - 1
  # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
  table.setdefault(pattern[-1], length)
  return table

def boyer_moore_search(text, pattern):
  # Створюємо таблицю зсувів для патерну (підрядка)
  shift_table = build_shift_table(pattern)
  i = 0 # Ініціалізуємо початковий індекс для основного тексту

  # Проходимо по основному тексту, порівнюючи з підрядком
  while i <= len(text) - len(pattern):
    j = len(pattern) - 1 # Починаємо з кінця підрядка

    # Порівнюємо символи від кінця підрядка до його початку
    while j >= 0 and text[i + j] == pattern[j]:
      j -= 1 # Зсуваємось до початку підрядка

    # Якщо весь підрядок збігається, повертаємо його позицію в тексті
    if j < 0:
      return i # Підрядок знайдено

    # Зсуваємо індекс i на основі таблиці зсувів
    # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
    i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

  # Якщо підрядок не знайдено, повертаємо -1
  return -1

# text = "Being a developer is not easy"
# pattern = "developer"

# position = boyer_moore_search(text, pattern)
# if position != -1:
#   print(f"Substring found at index {position}")
# else:
#   print("Substring not found")

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

# raw = "Цей алгоритм часто використовується в текстових редакторах та системах пошуку для ефективного знаходження підрядка в тексті."

# pattern = "алг"

# print(kmp_search(raw, pattern))

def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)

    # Базове число для хешування та модуль
    base = 256
    modulus = 101  

    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus

    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

# main_string = "Being a developer is not easy"
# substring = "developer"

# position = rabin_karp_search(main_string, substring)
# if position != -1:
#     print(f"Substring found at index {position}")
# else:
#     print("Substring not found")

def load_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except IOError:
        print(f"Error: Could not read file '{file_path}'.")
        return None
    
def benchmark_search(algorithm, text, pattern):
    timer = timeit.Timer(lambda: algorithm(text, pattern))
    return timer.timeit(number=100)

def print_comparison_table(results):
    # Виводимо заголовок таблиці
    print(f"{'Алгоритм':<10} {'Підрядок':<12} {'article01 (секунди)':<20} {'article02 (секунди)':<20}")
    print("=" * 62)

    # Додаємо дані в таблицю
    for algorithm, data in results.items():
        print(f"{algorithm:<10} {'Реальний':<12} {data['article01']['real']:<20.6f} {data['article02']['real']:<20.6f}")
        print(f"{algorithm:<10} {'Вигаданий':<12} {data['article01']['fake']:<20.6f} {data['article02']['fake']:<20.6f}")

def main():
    text1 = load_text('article01.txt')
    text2 = load_text('article02.txt')

    # Список алгоритмів
    algorithms = [("BM", boyer_moore_search), 
                  ("KMP", kmp_search), 
                  ("RK", rabin_karp_search)]

    results = {
        "BM": {"article01": {}, "article02": {}},
        "KMP": {"article01": {}, "article02": {}},
        "RK": {"article01": {}, "article02": {}},
    }

    real_pattern = "Література"  # Підрядок, що існує в тексті. Знаходиться в кінці тексту.
    fake_pattern = "Абра Кадабра"   # Підрядок, що не існує в тексті

    #article01
    for name, algorithm in algorithms:
        real_time = benchmark_search(algorithm, text1, real_pattern)
        fake_time = benchmark_search(algorithm, text1, fake_pattern)
        results[name]["article01"]["real"] = real_time
        results[name]["article01"]["fake"] = fake_time

    #article02
    for name, algorithm in algorithms:
        real_time = benchmark_search(algorithm, text2, real_pattern)
        fake_time = benchmark_search(algorithm, text2, fake_pattern)
        results[name]["article02"]["real"] = real_time
        results[name]["article02"]["fake"] = fake_time


    print("Шуканий рядок знаходиться в кінці тексту")
    print()
    print_comparison_table(results)

    real_pattern = "Анотація"  # Підрядок, що існує в тексті. знаходиться на початку тексту.
    fake_pattern = "Абра Кадабра"   # Підрядок, що не існує в тексті

    #article01
    for name, algorithm in algorithms:
        real_time = benchmark_search(algorithm, text1, real_pattern)
        fake_time = benchmark_search(algorithm, text1, fake_pattern)
        results[name]["article01"]["real"] = real_time
        results[name]["article01"]["fake"] = fake_time

    #article02
    for name, algorithm in algorithms:
        real_time = benchmark_search(algorithm, text2, real_pattern)
        fake_time = benchmark_search(algorithm, text2, fake_pattern)
        results[name]["article02"]["real"] = real_time
        results[name]["article02"]["fake"] = fake_time

    print()
    print("Шуканий рядок знаходиться на початку тексту")
    print()
    print_comparison_table(results)



    real_pattern = "Інтерполяційний пошук використовується для пошуку елементів у відсортованому масиві"  # Довгий підрядок
    fake_pattern = "Абра Кадабра"   # Підрядок, що не існує в тексті

    #article01
    for name, algorithm in algorithms:
        real_time = benchmark_search(algorithm, text1, real_pattern)
        fake_time = benchmark_search(algorithm, text1, fake_pattern)
        results[name]["article01"]["real"] = real_time
        results[name]["article01"]["fake"] = fake_time

    real_pattern = "Створена програмна імітаційна модель рекомендаційної системи для проведення експериментів"  # Довгий підрядок

    #article02
    for name, algorithm in algorithms:
        real_time = benchmark_search(algorithm, text2, real_pattern)
        fake_time = benchmark_search(algorithm, text2, fake_pattern)
        results[name]["article02"]["real"] = real_time
        results[name]["article02"]["fake"] = fake_time

    print()
    print("Пошук довгого підрядка")
    print()
    print_comparison_table(results)

if __name__ == "__main__":
    main()

# Висновки у файлі README.md