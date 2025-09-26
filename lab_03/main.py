import time
import threading
import random

smoker_semaphores = [threading.Semaphore(0) for _ in range(3)]
agent_semaphore = threading.Semaphore(1)

table_ingredients = [None, None]
is_running = True


def agent():
    global table_ingredients
    ingredients = ['табак', 'бумага', 'спички']

    while is_running:
        agent_semaphore.acquire()

        if not is_running:
            break

        chosen_ingredients = random.sample(ingredients, 2)
        table_ingredients = chosen_ingredients

        missing_ingredient = list(
            set(ingredients) - set(chosen_ingredients))[0]

        print(
            f"Посредник положил: {chosen_ingredients[0]}, {chosen_ingredients[1]} (нет: {missing_ingredient})")

        smoker_index = ingredients.index(missing_ingredient)

        smoker_semaphores[smoker_index].release()


def smoker(name, owned_ingredient, index):
    while is_running:
        smoker_semaphores[index].acquire()

        if not is_running:
            break

        print(f"{name} скручивает сигарету...")
        time.sleep(random.uniform(0.5, 1.5))

        print(f"{name} курит")
        time.sleep(random.uniform(1, 2))

        print(f"{name} закончил курить")

        table_ingredients[0] = None
        table_ingredients[1] = None
        agent_semaphore.release()


if __name__ == '__main__':
    try:
        agent_thread = threading.Thread(target=agent, daemon=True)
        agent_thread.start()

        smokers_info = [
            ("Курильщик с табаком", "табак", 0),
            ("Курильщик с бумагой", "бумага", 1),
            ("Курильщик со спичками", "спички", 2)
        ]

        smoker_threads = []
        for info in smokers_info:
            thread = threading.Thread(target=smoker, args=info, daemon=True)
            smoker_threads.append(thread)
            thread.start()

        print("Начало работы")
        time.sleep(10)

    finally:
        print("Завершение работы")
        is_running = False

        agent_semaphore.release()
        for sem in smoker_semaphores:
            sem.release()
