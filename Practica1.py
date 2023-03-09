from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import current_process
from multiprocessing import Value, Array
import random

N = 10
NPROD = 3

def producer(i, storage, empty, non_empty):
    current = 0 
    for v in range(N):
        empty.acquire()
        print (f"producer {current_process().name} produciendo")
        current += random.randint(0,5)
        storage[i] = current
        non_empty.release()
        print (f"producer {current_process().name} almacenado {current}")
    empty.acquire()
    storage[i] = -1
    non_empty.release()


def consumer(storage: list[Value], empty: list[BoundedSemaphore], non_empty):
    for i in range(NPROD):
        non_empty[i].acquire()
    print (f"consumer {current_process().name} desalmacenando")
    listafinal = []
    while max(storage) != -1:
        index = 0
        a = (index, max(storage))
        print(max(storage))
        for i in range(len(storage)):
            if 0 <= storage[i] <= a[1]:
                a = (i, storage[i])
        print (f"consumer {current_process().name} consumiendo {a[1]}")
        listafinal.append(a[1])
        empty[a[0]].release()
        non_empty[a[0]].acquire()
    print("He consumido todo esto, ")
    print(listafinal)

def main():
    storage = Array('i', NPROD)
    for i in range(NPROD):
        storage[i] = -2
    print ("almacen inicial", storage[:])
    
    non_empty = [Semaphore(0) for _ in range(NPROD)]
    empty = [BoundedSemaphore(1) for _ in range(NPROD)]

    prodlst = [ Process(target=producer, name=f'prod_{i}', args=(i, storage,  empty[i], non_empty[i]))
                for i in range(NPROD) ]
    
    conslst = Process(target=consumer,
                      name=f"cons_{i}",
                      args=(storage, empty, non_empty))

    for p in prodlst:
        p.start()
    conslst.start()
    for p in prodlst:
        p.join()
    conslst.join()

if __name__ == '__main__':
    main()
 