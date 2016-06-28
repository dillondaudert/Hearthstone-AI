import multiprocessing as mp
import sys

def callb(result):
    print(result)
    sys.stdout.flush()

def act(a, b, index):
    c = a + b
    q_vals[index] = c
    return c
    

q_vals = mp.Array('f', 5)
for i in range(5):
    q_vals[i] = 0.0

a = [(1., 2., 0), (2., 3., 1), (3., 4., 2)]

with mp.Pool() as pool:
    for tupl in a:
        pool.apply_async(act, tupl, callback=callb)
        
    pool.close()
    pool.join()

print(list(q_vals))
