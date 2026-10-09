from multiprocessing import Process
import time

def take_order():
    for i in range(1,4):
        print(f"Order taken for #{i}")
        time.sleep(1)

def brew_chai():
    for i in range(1,4):
        print(f"Brew chai for #{i}")
        time.sleep(1)

#parallel execution
if __name__=="__main__":
    order_process= Process(target=take_order)
    brew_process = Process(target=brew_chai)

    order_process.start()
    brew_process.start()

    order_process.join()
    brew_process.join()

    print(f"All orders taken and chai brewed")
