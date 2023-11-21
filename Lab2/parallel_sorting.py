import time
import os
import numpy as np
import multiprocessing as mp

LEN_RUN = 32
num_process = os.cpu_count()

def insertionSort(arr):
    for i in range(len(arr)):
        j = i
        while j > 0 and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1
    return arr

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def parallel_sort(arr): 
    runs = []
    for i in range(0, len(arr), LEN_RUN):
        runs.append(arr[i:i + LEN_RUN])
        
    pool = mp.Pool(num_process)
    runs_Sorted = pool.map(insertionSort, runs)
    pool.close()
    pool.join()
   
    while (len(runs_Sorted) != 1):
        res = []
        for i in range(0,len(runs_Sorted)-1, 2):
            res.append(np.array(merge(runs_Sorted[i], runs_Sorted[i+1])))
        if (len(runs_Sorted)%2 == 1):
            res.append(runs_Sorted[len(runs_Sorted) - 1])
        runs_Sorted = res
    return runs_Sorted[0]
    

if __name__ == '__main__':
    numbers = np.random.randint(low=-5000000, high=5000000, size=100000)
    start = time.time()
    print(parallel_sort(numbers))
    end = time.time()
    print(end - start)