def insertion_sort(array):
    length = len(array)

    for i in range(length):
        for j in range(i, 0, -1):

            if j > 0 and array[j - 1] > array[j]:
                array[j - 1], array[j] = array[j], array[j - 1]

    return array


print(insertion_sort([1, 2, 3, 4, 5, 6, 7, 8]))
print(insertion_sort([8, 7, 6, 5, 4, 3, 2, 1]))
print(insertion_sort([3, 7, 4, 8, 1, 5, 2, 6]))