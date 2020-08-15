import time

def count_infinite():
    num = 0
    while True:
        yield num
        num += 1

def count_sheep():
    for i in count_infinite():
        print(f"{i} sheep sleeping peacefully")
        time.sleep(3)

   
    
from matplotlib import pyplot as plt
plt.ion()
i = 0
while True:
    plt.plot([0,i],[i,i])
    input("???")
    i+=1
    (i)