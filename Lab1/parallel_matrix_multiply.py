import time
import multiprocessing as mp
import numpy as np


num_process = 8

def parallel_multiply_matrices(A, B):
    chunk_size = len(A)//num_process
    chunks_A = [A[i: i+chunk_size] for i in range(0, len(A), chunk_size)]
    reversed_B = revert_matrix(B)
    
    pool = mp.Pool(num_process)
    temp_matrix = pool.starmap(chunk_multiply_matrices, [(chunks_A[i], reversed_B) for i in range(len(chunks_A))])
    pool.close()
    pool.join()
    results = np.concatenate(temp_matrix)
        
    return results

def chunk_multiply_matrices(chunk, matrix):
    rows = np.zeros((len(chunk), len(matrix[0])))
    for i in range(len(chunk)):
        for j in range(len(matrix)): 
            rows[i][j] = multiply_one(chunk[i], matrix[j]) 
    return rows

def revert_matrix(matrix):
    result = np.zeros((len(matrix), len(matrix[0])))
    for i in range(len(result)):
        result[i] = get_col(matrix, i)
    return result    
    

def get_col(matrix, col_index):
    column = [row[col_index] for row in matrix]
    return column

def multiply_one(row, col):
    result = 0
    for i in range(len(row)):
        result += row[i]*col[i]
    return result

if __name__ == '__main__':
    A = np.random.randint(100, 1000, size = (1000, 1000))
    B = np.random.randint(600, 6000, size = (1000, 1000))    
    
    start = time.perf_counter()
    print(parallel_multiply_matrices(A,B))   
    end = time.perf_counter()
    print(end - start)