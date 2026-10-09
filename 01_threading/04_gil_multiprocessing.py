from multiprocessing import Process
import time


def crunch_number():
    print(f"{Process().name} count processing....")
    count=0
    for _ in range(100_000_000):
        count+=1
    print(f"{Process().name} done")

if __name__=="__main__":
    start= time.time()
    p1=Process(target=crunch_number, name="Cruncher-1")
    p2=Process(target=crunch_number, name="Cruncher-2")

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    end= time.time()
    print(f"Total time taken: {end-start:.2f} seconds")
