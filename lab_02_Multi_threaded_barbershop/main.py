"""Модель задачи о многопотечной парикмахерской.

Парикмахер и клиенты взаимодействуют через семафоры.
"""

import threading
import time
import random

HAIRCUT_TIME = (1, 2)
CLIENT_GENERATION_TIME = (0.3, 1.0)
MAX_CHAIRS = 3


class BarberShop:
    """Модель многопотечной парикмахерской."""

    def __init__(self):
        self.waiting_customers = 0
        self.customers = threading.Semaphore(0)
        self.barber = threading.Semaphore(0)
        self.mutex = threading.Semaphore(1)

    def barber_thread(self):
        """Поведение парикмахера: ждет клиента и стрижет."""
        while True:
            print("Парикмахер ждет клиента")
            self.customers.acquire()

            with self.mutex:
                self.waiting_customers -= 1
                self.barber.release()

            print("Парикмахер стрижет")
            time.sleep(random.uniform(*HAIRCUT_TIME))
            print("Парикмахер закончил стрижку")

    def customer_thread(self, customer_id):
        """Поведение клиента: ждет место или уходит."""
        with self.mutex:
            if self.waiting_customers < MAX_CHAIRS:
                self.waiting_customers += 1
                print(f"Клиент {customer_id} ждет ({self.waiting_customers})")
                self.customers.release()
            else:
                print(f"Клиент {customer_id} ушел - нет мест")
                return  # клиент ушел, не ждём стрижки

        self.barber.acquire()
        print(f"Клиент {customer_id} стрижется")


def main():
    """Запуск симуляции парикмахерской."""
    shop = BarberShop()
    threading.Thread(target=shop.barber_thread, daemon=True).start()

    customer_counter = 1
    while True:
        time.sleep(random.uniform(*CLIENT_GENERATION_TIME))
        threading.Thread(target=shop.customer_thread,
                         args=(customer_counter,)).start()
        customer_counter += 1


if __name__ == "__main__":
    main()
