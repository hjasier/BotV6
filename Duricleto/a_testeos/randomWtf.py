import random

opciones = ["test2","etsat"]
pesos = [0.20, 0.80]

for n in range(100):
    choice = random.choices(opciones, weights=pesos)[0]
    print(choice)