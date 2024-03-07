

# 5 Karten ziehen
# dann die Zahlen jeweils zu orden mit Modulo 13
# Durch Modulo 13 weiß man welche Kartenfarbe man erhält
# der Rest aus dem Modulo dient dazu die Kartenfarbe zu bestimmen: Herz,Pik,KreuzKaro
# Die Hauptaufgabe liegt darin heraus zu finden ob man ein paar hat oder nicht
# Methoden für ein Paar, zwei paar, Drilling etc
# dann Programm erweitern um eine Million mal zu ziehen

# set für nur eindeutige Elemente da Doppelte entfernt werden
# len berechnet die Anzahl der vorhandenen farben



from random import random, randint
import functools
import time
from random import sample

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


def pokerDeck():
    stapel = list(range(0, 52))
    gezogeneKarten = sample(stapel, 5)
    return gezogeneKarten




def kartenBestimmen(karteid):
    farben = ["Herz", "Pik", "Karo", "Kreuz"]
    karteid_modulo = karteid % 13
    """return "Karte ist {} von {}".format(karteid_modulo + 1, farben[karteid // 13])"""


def hatPaar(karten):
    kartenwerte = [k % 13 for k in karten]
    paar_count = 0
    for karte in kartenwerte:
        if kartenwerte.count(karte) == 2:
            paar_count += 1
    return paar_count >= 1


def hatZweiPaare(karten):
    kartenwerte = [k % 13 for k in karten]
    wert_counts = {karte: kartenwerte.count(karte) for karte in kartenwerte}
    return list(wert_counts.values()).count(2) == 2


def hatDrilling(karten):
    kartenwerte = [k % 13 for k in karten]
    for karte in kartenwerte:
        if kartenwerte.count(karte) == 3:
            return True
    return False


def hatStrasse(karten):
    kartenwerte = [k % 13 for k in karten]
    eindeutige_werte = sorted(set(kartenwerte))

    if len(eindeutige_werte) < 5:
        return False
    if eindeutige_werte[-1] - eindeutige_werte[0] == 4:
        return True

    return False


def hatFlush(karten):
    referenz_farbe = karten[0] // 13

    for karte in karten:
        if karte // 13 != referenz_farbe:
            return False

    return True


def hatFullHouse(karten):
    kartenwerte = [k % 13 for k in karten]
    wert_counts = {karte: kartenwerte.count(karte) for karte in kartenwerte}

    hat_drilling = False
    hat_paar = False

    for wert, count in wert_counts.items():
        if count == 3:
            hat_drilling = True
        elif count == 2:
            hat_paar = True

    return hat_drilling and hat_paar


def hatFourOfAKind(karten):
    kartenwerte = [k % 13 for k in karten]
    wert_counts = {karte: kartenwerte.count(karte) for karte in kartenwerte}

    for count in wert_counts.values():
        if count == 4:
            return True

    return False


def hatStraightFlush(karten):
    kartenwerte = [k % 13 for k in karten]
    kartenfarben = [k // 13 for k in karten]

    if len(set(kartenfarben)) != 1:
        return False

    kartenwerte_eindeutig = sorted(set(kartenwerte))

    if len(kartenwerte_eindeutig) < 5:
        return False

    if kartenwerte_eindeutig[-1] - kartenwerte_eindeutig[0] == 4:
        return True

    return False


def hatRoyalFlush(karten):
    kartenwerte = [k % 13 for k in karten]
    kartenfarben = [k // 13 for k in karten]

    if len(set(kartenfarben)) != 1:
        return False

    kartenwerte_eindeutig = sorted(set(kartenwerte))

    royal_flush_werte = set([9, 10, 11, 12, 0])
    return royal_flush_werte == set(kartenwerte_eindeutig)




@timer
def startGame():
    cards = pokerDeck()
    print("Gezogene Karten:", cards)


    statistik = {
    "Paar": 0,
    "Zwei Paare": 0,
    "Drilling": 0,
    "Straße": 0,
    "Flush": 0,
    "Full House": 0,
    "Four of a Kind": 0,
    "Straight Flush": 0,
    "Royal Flush": 0
    }


    anzahl_zuege = 10000

    for i in range(anzahl_zuege):
        cards = pokerDeck()
        if hatRoyalFlush(cards):
            statistik["Royal Flush"] += 1
        elif hatStraightFlush(cards):
            statistik["Straight Flush"] += 1
        elif hatFourOfAKind(cards):
            statistik["Four of a Kind"] += 1
        elif hatFullHouse(cards):
            statistik["Full House"] += 1
        elif hatFlush(cards):
            statistik["Flush"] += 1
        elif hatStrasse(cards):
            statistik["Straße"] += 1
        elif hatDrilling(cards):
            statistik["Drilling"] += 1
        elif hatZweiPaare(cards):
            statistik["Zwei Paare"] += 1
        elif hatPaar(cards):
            statistik["Paar"] += 1


    for hand, anzahl in statistik.items():
        prozent = (anzahl / anzahl_zuege) * 100
        print(f"{hand}: {prozent:.10f}%")



if __name__ == '__main__':
    startGame()
