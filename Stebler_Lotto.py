# def hallo(name):
# for i in range(5):
# print(f"Hallo {name}")
# if name == 'ege':
# print("Geheiratet")
# hallo('ege')

# Liste 45 Zahlen
# eine ziehen zwischen 0 und 44
# nur index nicht di Zahl
# die Zahl dann auf index 20 ansehen und mit der letzten Stelle vertauschen
# Randomizer macht dann 0-43 mehr als schritt usw

# Ergebnisse in einem Dictionary festhalte

import random


def lotto(n):
    zahl_liste = list(range(1, 46))
    gezogen = {}

    for i in range(n):
        index = random.randint(0, 44)

        posS = zahl_liste[index]
        posE = zahl_liste[44 - i]

        zahl_liste[index] = posE
        zahl_liste[44 - i] = posS
        # zahl_liste[posS], zahl_liste[posE] = zahl_liste[posE], zahl_liste[posS]
        # Weniger Zeilen um zu vertauschen posS,posE=posE,posS

        # In Dic speichern und die Häufigkeit zählen
        gezogene_zahl = posS
        if gezogene_zahl not in gezogen:
            gezogen[gezogene_zahl] = 1
        else:
            gezogen[gezogene_zahl] += 1

    return gezogen


def statistik():
    anz_gezogen = {}
    for zahl in range(1, 46):
        anz_gezogen[zahl] = 0

    return anz_gezogen


statistik_dict = statistik()

for i in range(1000):
    ergebnis = lotto(6)
    for gezogene_zahl, häufigkeit in ergebnis.items():
        statistik_dict[gezogene_zahl] += häufigkeit
        # += ... statistik_dict[gezogene_zahl] = statistik_dict[gezogene_zahl] + häufigkeit

for zahl, häufigkeit in statistik_dict.items():
    print(f"Zahl {zahl}: {'|' * häufigkeit}{häufigkeit}")

