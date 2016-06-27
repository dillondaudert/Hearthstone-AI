import multiprocessing as mp

def callb(result):
    print(result)

def act(a, b):
    c = a + b
    print(c)

a = [(1, 2), (2, 3), (3, 4)]
arg1 = 'hi'
arg2 = 'lo'
arg3 = 5

with mp.Pool() as pool:
    pool.apply(act, a)
