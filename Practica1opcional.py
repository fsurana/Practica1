from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import current_process
from multiprocessing import Value, Array
import random

N = 10
NPROD = 3
Huecos = 2

def producer(i, almacen, empty, non_empty):
    current = 0
    indice = 0 # donde vamos a escribir
    for v in range(N):
        empty.acquire()
        print (f"{current_process().name} produciendo\n")
        current += random.randint(0,5)
        almacen[indice] = current
        indice = (indice + 1) % Huecos
        non_empty.release()
        print (f"{current_process().name} almacenado {list(almacen)}\n")
        
    empty.acquire()
    almacen[indice] = -1
    non_empty.release()


def consumer(almacen, empty: list[BoundedSemaphore], non_empty):
    listafinal = []
    indice_lec = [0 for _ in range(NPROD)]
    lista = [-1 for _ in range(NPROD)]
    
    for i in range(NPROD):
        non_empty[i].acquire()
    
    lectura = []
    for i in range(NPROD):
        lectura.append(almacen[i][0])

    while lectura != lista:
        print ("consumer desalmacenando\n")
        (a,b) = minimo(lectura)
        indice_lec[a] = (indice_lec[a] + 1) % Huecos
        print (f"consumer consumiendo {b}\n")
        non_empty[a].acquire()
        empty[a].release()
        lectura[a] = almacen[a][indice_lec[a]]
        listafinal.append(b)


    print("He consumido todo esto, ")
    print(listafinal)
    print(f"Un número total de {len(listafinal)} ")

def minimo(lista):
    (a,b) = (0, lista[0])
    while b == -1:
        (a,b) = (a + 1, lista[a])
        
    for i in range(len(lista)):
        if 0 <= lista[i] <= b:
            (a,b) = (i, lista[i])
    
    return (a,b)

def main():

    almacenes = []
        
    for i in range (NPROD):
        storage = Array('i', Huecos)
        for i in range(Huecos):
            storage[i] = -2
        almacenes.append(storage)
    print ("El almacén inicial es de esta forma", almacenes[i])
    
    non_empty = [Semaphore(0) for _ in range(NPROD)]
    empty = [BoundedSemaphore(Huecos) for _ in range(NPROD)]
 
    prodlst = [ Process(target=producer, name=f'prod_{i}', args=(i, almacenes[i],  empty[i], non_empty[i]))
                for i in range(NPROD) ]
    
    conslst = Process(target=consumer,
                      name=f"cons_{i}",
                      args=(almacenes, empty, non_empty))

    for p in prodlst:
        p.start()
    conslst.start()
    for p in prodlst:
        p.join()
    conslst.join()

if __name__ == '__main__':
    main()