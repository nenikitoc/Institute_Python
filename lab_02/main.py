import threading
import time
import random

HAIRCUT_TIME = (1, 2)
CLIENT_GENERATION_TIME = (0.3, 1.0)

customers = threading.Semaphore(0)
barber = threading.Semaphore(0)
mutex = threading.Semaphore(1)

waiting_customers = 0
max_chairs = 3


def barber_thread():
    while True:
        print("Парикмахер ждет клиента")
        customers.acquire()

        mutex.acquire()
        waiting_customers -= 1
        barber.release()
        mutex.release()

        print("Парикмахер стрижет")
        time.sleep(random.uniform(*HAIRCUT_TIME))
        print("Парикмахер закончил стрижку")


def customer_thread(customer_id):
    global waiting_customers

    mutex.acquire()

    if waiting_customers < max_chairs:
        waiting_customers += 1
        print(f"Клиент {customer_id} ждет ({waiting_customers})")
        customers.release()
        mutex.release()

        barber.acquire()
        print(f"Клиент {customer_id} стрижется")
    else:
        print(f"Клиент {customer_id} ушел - нет мест")
        mutex.release()


if __name__ == "__main__":
    threading.Thread(target=barber_thread, daemon=True).start()

    customer_id = 1
    while True:
        time.sleep(random.uniform(*CLIENT_GENERATION_TIME))
        threading.Thread(target=customer_thread, args=(customer_id,)).start()
        customer_id += 1
