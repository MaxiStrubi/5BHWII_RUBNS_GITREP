class Person:
    def __init__(self, name, geschlecht):
        self.name = name
        self.geschlecht = geschlecht


class Mitarbeiter(Person):
    def __init__(self, name, geschlecht):
        super().__init__(name, geschlecht)
        self.abteilung = None


class Abteilungsleiter(Mitarbeiter):
    def __init__(self, name, geschlecht):
        super().__init__(name, geschlecht)

    # def __str__(self):
    # return f"firstname"+ self.name


class Abteilung:
    def __init__(self, name):
        self.name = name
        self.mitarbeiter = []
        self.abteilungsleiter = None
        # keine List weil nur einer

    def appendMitarbeiter(self, mitarbeiter):
        self.mitarbeiter.append(mitarbeiter)
        mitarbeiter.abteilung = self

    def setAbteilungsleiter(self, abteilungsleiter):
        self.abteilungsleiter = abteilungsleiter
        if abteilungsleiter not in self.mitarbeiter:
            self.appendMitarbeiter(abteilungsleiter)


class Firma:
    def __init__(self):
        self.abteilungen = []

    def anzahlMitarbeiter(self):
        gesamtanzahlMitarbeiter = 0
        for abteilung in self.abteilungen:
            anzahlMitarbeiterInAbteilung = len(abteilung.mitarbeiter)
            gesamtanzahlMitarbeiter += anzahlMitarbeiterInAbteilung

        return gesamtanzahlMitarbeiter

    def anzahlAbteilungsleiter(self):
        gesamtanzahlAbteilungsleiter = 0
        for abteilung in self.abteilungen:
            gesamtanzahlAbteilungsleiter += 1

        return gesamtanzahlAbteilungsleiter

    def abteilungMitMeistenMitarbeitern(self):
        if not self.abteilungen:
            return "Keine Abteilung"

        maxMitarbeiteranzahl = 0
        max_abteilung = None

        for abteilung in self.abteilungen:
            anzahlMitarbeiter = len(abteilung.mitarbeiter)

            if anzahlMitarbeiter > maxMitarbeiteranzahl:
                maxMitarbeiteranzahl = anzahlMitarbeiter
                max_abteilung = abteilung

        return max_abteilung.name if max_abteilung else "Keine Abteilung"

    def prozentAnteilGeschlecht(self):
        gesamtzahlMitarbeiter = self.anzahlMitarbeiter()

        if gesamtzahlMitarbeiter == 0:
            return {'männlich': 0, 'weiblich': 0}

        anzahlMaenner = 0

        for abteilung in self.abteilungen:
            for mitarbeiter in abteilung.mitarbeiter:
                if mitarbeiter.geschlecht == 'männlich':
                    anzahlMaenner += 1

        prozentMännlich = (anzahlMaenner / gesamtzahlMitarbeiter) * 100
        prozentWeiblich = 100 - prozentMännlich

        prozentDict = {'männlich': prozentMännlich, 'weiblich': prozentWeiblich}
        return prozentDict


if __name__ == "__main__":
    SweettecFirma = Firma()

    for abt in ["IT", "HR", "Marketing"]:
        SweettecFirma.abteilungen.append(Abteilung(abt))

    m1 = Mitarbeiter("Peppi", "weiblich")
    m2 = Mitarbeiter("Flo", "männlich")
    m3 = Mitarbeiter("Much", "männlich")

    a1 = Abteilungsleiter("Peter", "weiblich")
    a2 = Abteilungsleiter("Magnussen", "männlich")

    SweettecFirma.abteilungen[0].appendMitarbeiter(m1)
    SweettecFirma.abteilungen[0].appendMitarbeiter(m2)
    SweettecFirma.abteilungen[1].appendMitarbeiter(m3)

    SweettecFirma.abteilungen[0].setAbteilungsleiter(a1)
    SweettecFirma.abteilungen[1].setAbteilungsleiter(a2)

    print("Anzahl Mitarbeiter:", SweettecFirma.anzahlMitarbeiter())
    print("Anzahl Abteilungsleiter:", SweettecFirma.anzahlAbteilungsleiter())
    print("Abteilung mit den meisten Mitarbeitern:", SweettecFirma.abteilungMitMeistenMitarbeitern())
    print("Prozentualer Anteil von Geschlechtern:", SweettecFirma.prozentAnteilGeschlecht())