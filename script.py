from datetime import datetime
import time
import sys
counter_compare = 0
counter_replace = 0

server_file = sys.argv[1]

handle = open(server_file, "r")
Heap_array = handle.read()
handle.close()
print(Heap_array)
Heap_array = Heap_array.split()
print(Heap_array)
for i in range(0, len(Heap_array)):
    Heap_array[i] = int(Heap_array[i])
print(type(Heap_array))
print(Heap_array)
print("Array before shell", Heap_array )

start_time = datetime.now()
s = ''' '''
def heapify(arr, n, i):
    # Find largest among root and children
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2 
 
    if l < n and arr[i] < arr[l]:
        largest = l
 
    if r < n and arr[largest] < arr[r]:
        largest = r
 
    # If root is not largest, swap with largest and continue heapifying
    if largest != i:
        arr[i],arr[largest] = arr[largest],arr[i]
        heapify(arr, n, largest)
 
def heapSort(arr):
    n = len(arr)
 
    # Build max heap
    for i in range(n, 0, -1):
        heapify(arr, n, i)
 
 
    for i in range(n-1, 0, -1):
        # swap
        arr[i], arr[0] = arr[0], arr[i]  
 
        #heapify root element
        heapify(arr, i, 0)
 
 
arr = Heap_array
heapSort(arr)
print('Array after shaker', Heap_array )
print(" Lenght:", len(Heap_array))
print("Time:")
print(datetime.now() - start_time)
for i in range(0, len(Heap_array)):
    shell_array[i] = str(Heap_array[i])
result =''.join(Heap_array)
handle = open("server_outcoming.txt", "w")
handle.write(result)
handle.close()
