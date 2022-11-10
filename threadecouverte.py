import threading
import time


if __name__ == '__main__':
    def task(i):
        print(f"Task {i} starts")
        time.sleep(1)
        print(f"Task {i} ends")

    start = time.perf_counter()
    t1 = threading.Thread(target=task, args=[1])
    t2 = threading.Thread(target=task, args=[2])
    t1.start() # lancement des deux threads en meme temps (a peu près)
    t2.start()
    t1.join() # fin des deux threads
    t2.join()
    end = time.perf_counter()
    print(f"Tasks ended in {round(end - start, 2)} second(s)")

    # Test avec 50 Threads

    T = []
    for i in range(50):
        T.append(threading.Thread(target=task, args=[i]))

    for i in range(len(T)):
        T[i].start()

    for i in range(len(T)):
        T[i].join()