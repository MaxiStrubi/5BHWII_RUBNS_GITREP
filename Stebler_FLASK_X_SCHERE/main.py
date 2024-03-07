import json
import random
import requests

# Definiert die verfügbaren Optionen und ihre entsprechenden Werte
optionen = {"Stein": 1, "Papier": 2, "Schere": 3, "Echse": 4, "Spock": 5}

def start_menu(spiel_id, verlauf):
    print("\n1: Spielregeln anzeigen\n2: Spielstatistik anzeigen\n3: Neues Spiel starten\n4: Spielverlauf speichern")
    auswahl = input("Wählen Sie eine Option: ")

    if auswahl == '1':
        zeige_regeln()
    elif auswahl == '2':
        zeige_statistik(verlauf)
    elif auswahl == '3':
        neues_spiel(spiel_id, verlauf)
    elif auswahl == '4':
        speichere_verlauf(verlauf)
    else:
        print("Falsche Eingabe, bitte versuchen Sie es erneut.")
        start_menu(spiel_id, verlauf)

def zeige_statistik(verlauf):
    spieler_siege, bot_siege, unentschieden = 0, 0, 0
    symbol_zähler = {"Stein": 0, "Papier": 0, "Schere": 0, "Echse": 0, "Spock": 0}

    if not verlauf:
        print("Keine Spiele gespielt.")
    else:
        for spiel in verlauf:
            ergebnis = spiel["ergebnis"]
            spieler_siege += ergebnis == "spieler"
            bot_siege += ergebnis == "bot"
            unentschieden += ergebnis == "unentschieden"

            spieler_wahl = spiel["spieler"]
            symbol_liste = [k for k, v in optionen.items() if v == spieler_wahl]

            if symbol_liste:
                symbol = symbol_liste[0]
                symbol_zähler[symbol] += 1
            else:
                print(f"Warnung: Ungültige Spielerwahl {spieler_wahl} gefunden.")

        gesamtspiele = len(verlauf)
        print(f"Insgesamt wurden {gesamtspiele} Spiele gespielt:")
        print(f"Der Spieler hat {spieler_siege} Mal gewonnen")
        print(f"Der Bot hat {bot_siege} Mal gewonnen")
        print(f"Es gab {unentschieden} Mal ein Unentschieden\n")
        for symbol, anzahl in symbol_zähler.items():
            print(f"{symbol}: {anzahl} Mal gewählt")
        send_symbol_data_to_server(symbol_zähler)

def neues_spiel(spiel_id, verlauf):
    auswahl = input("Wählen Sie: Stein(1), Papier(2), Schere(3), Echse(4), Spock(5): ")

    if auswahl.isdigit() and 1 <= int(auswahl) <= 5:
        spieler_auswahl = int(auswahl)
        bot_auswahl = random.choice(list(optionen.values()))
        print(f"Bot wählt: {bot_auswahl}")
        ergebnis = ermitteln_gewinner(spieler_auswahl, bot_auswahl)
        spiel_fortsetzen(ergebnis, spiel_id, verlauf)
    else:
        print("Falsche Eingabe, bitte versuchen Sie es erneut.")
        spiel_fortsetzen({"spieler": "Fehler", "bot": "Fehler", "ergebnis": "Fehler"}, spiel_id, verlauf)

def ermitteln_gewinner(spieler, bot):
    if spieler == bot:
        print("Unentschieden")
        return {"spieler": spieler, "bot": bot, "ergebnis": "Unentschieden"}

    # Prüft alle Gewinnbedingungen für den Spieler
    gewinnbedingungen = [
        (spieler == optionen["Schere"] and bot in [optionen["Papier"], optionen["Echse"]]),
        (spieler == optionen["Papier"] and bot in [optionen["Stein"], optionen["Spock"]]),
        (spieler == optionen["Stein"] and bot in [optionen["Schere"], optionen["Echse"]]),
        (spieler == optionen["Echse"] and bot in [optionen["Spock"], optionen["Papier"]]),
        (spieler == optionen["Spock"] and bot in [optionen["Schere"], optionen["Stein"]]),
    ]

    if any(gewinnbedingungen):
        print("Spieler gewinnt!")
        return {"spieler": spieler, "bot": bot, "ergebnis": "Spieler"}
    else:
        print("Bot gewinnt.")
        return {"spieler": spieler, "bot": bot, "ergebnis": "Bot"}

def spiel_fortsetzen(ergebnis, spiel_id, verlauf):
    spiel_id += 1
    verlauf.append({"spielId": spiel_id, **ergebnis})
    #speichere_spiel(verlauf)
    weiter = input("Möchten Sie weiter spielen (j/n)? ")


    if weiter.lower() == 'j':
        neues_spiel(spiel_id, verlauf)
    elif weiter.lower() == 'n':
        start_menu(spiel_id, verlauf)
    else:
        print("Falsche Eingabe, bitte versuchen Sie es erneut.")
        start_menu(spiel_id, verlauf)

def zeige_regeln():
    regeln = (
        "Schere schneidet Papier, Papier bedeckt Stein, Stein zerquetscht Echse, "
        "Echse vergiftet Spock, Spock zerschlägt Schere, Schere köpft Echse, "
        "Echse frisst Papier, Papier widerlegt Spock, Spock verdampft Stein, "
        "und wie es immer war, Stein schleift Schere."
    )
    print(regeln)

def speichere_verlauf(verlauf):
    try:
        with open('spielverlauf.json', 'w') as datei:
            json.dump(verlauf, datei)
        print("Spielverlauf gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern: {e}")


def send_symbol_data_to_server(symbol_zähler):
    url = "http://localhost:5000/SaveSymbolStats"
    try:
        response = requests.post(url, json=symbol_zähler)
        if response.status_code == 200:
            print("Daten erfolgreich an den Server übertragen.")
        else:
            print(f"Fehler bei der Übertragung: {response.status_code}")
    except requests.RequestException as e:
        print(f"Verbindungsfehler: {e}")



if __name__ == "__main__":
    try:
        with open('spielverlauf.json', 'r') as datei:
            geladene_daten = json.load(datei)
            spiel_id = geladene_daten[-1]['spielId'] if geladene_daten else 0
            print("Letzte Spiel-ID:", spiel_id)
    except (FileNotFoundError, json.JSONDecodeError):
        geladene_daten = []
        spiel_id = 0
        print("Kein vorheriger Spielverlauf gefunden.")

    start_menu(spiel_id, geladene_daten)
