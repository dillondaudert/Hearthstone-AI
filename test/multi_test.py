import multiprocessing as mp
from time import sleep
from os import getpid


class ThisError(Exception):
    def __init__(self, message):
        super(ThisError, self).__init__("An exception of This Error")
        self.message = message

def function(a):
    if a:
        raise ThisError("Child process %s failed!" % mp.current_process().name)
    else:
        return "true"

def callb(result):
    print(result)

def err_callb(exception):
    print(exception.message)
    print(type(exception))

def main():
    with mp.Pool() as pool:
        result1 = pool.apply_async(function, (True,), callback=callb, error_callback=err_callb)
        result2 = pool.map_async(function, (False,), callback=callb, error_callback=err_callb)
        while(not (result1.ready() and result2.ready()) ):
            sleep(1)

    print(result1.successful())
    print(result2.successful())

if __name__ == "__main__":
    main()
