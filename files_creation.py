import random
value = 4000
name_file = "incoming.txt"


items = [random.randint(0, value) for i in range(value)]
for i in range(0, len(items)):
    items[i] = str(items[i])
numbers =  ' '.join(items)
handle = open(name_file, "w")
handle.write(numbers)
handle.close()
print("Done")
