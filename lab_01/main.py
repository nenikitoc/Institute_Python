import threading
import time
import random

NUM_PHILOSOPHERS = 5
THINK_TIME = (1, 5)
EAT_TIME = (3, 4)

forks = [threading.Semaphore(1) for _ in range(NUM_PHILOSOPHERS)]

def philosopher(philosopher_id):
    left_fork = philosopher_id
    right_fork = (philosopher_id + 1) % NUM_PHILOSOPHERS

    while True:
        think_time = random.uniform(*THINK_TIME)
        print(f"Философ {philosopher_id} размышляет {think_time:.1f} сек.")
        time.sleep(think_time)

        first_fork = min(left_fork, right_fork)
        second_fork = max(left_fork, right_fork)

        print(f"Философ {philosopher_id} пытается взять вилки {first_fork} и {second_fork}")
        forks[first_fork].acquire()
        forks[second_fork].acquire()
        
        eat_time = random.uniform(*EAT_TIME)
        print(f"Философ {philosopher_id} ест {eat_time:.1f} сек.")
        time.sleep(eat_time)
        
        forks[second_fork].release()
        forks[first_fork].release()

if __name__ == "__main__":
    threads = []
    for i in range(NUM_PHILOSOPHERS):
        t = threading.Thread(target=philosopher, args=(i,))
        t.daemon = True
        threads.append(t)
        t.start()
        
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем")
