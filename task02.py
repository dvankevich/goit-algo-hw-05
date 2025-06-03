'''
Реалізуйте двійковий пошук для відсортованого масиву з дробовими числами. 
Написана функція для двійкового пошуку повинна повертати кортеж, де першим 
елементом є кількість ітерацій, потрібних для знаходження елемента. 
Другим елементом має бути "верхня межа" — це найменший елемент, який є більшим 
або рівним заданому значенню.
'''

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    iter = 0

    while low <= high:
        iter+=1
        mid = (high + low) // 2
        # print(f'low: {arr[low]} high: {arr[high]} mid {arr[mid]} iteration {iter}')
        # якщо x більше за значення посередині списку, ігноруємо ліву половину
        if arr[mid] < x:
            low = mid + 1

        # якщо x менше за значення посередині списку, ігноруємо праву половину
        elif arr[mid] > x:
            high = mid - 1

        # інакше x присутній на позиції і повертаємо його
        else:
            #print(f'low: {arr[low]} high: {arr[high]} mid {arr[mid]} iteration {iter}')
            break
        
    return (iter, arr[high])

arr = [1.1, 3.3, 5.3, 8.8, 10.1, 12.12, 15.15, 18.18, 20.2, 22.2, 24.4]
print(arr)
for x in arr:
    iterations, high = binary_search(arr, x)
    print(f"x={x} Iterations {iterations} high {high}")

x = 16.6 # значення якого немає в масиві
iterations, high = binary_search(arr, x)
print(f"x={x} Iterations {iterations} high {high}")
