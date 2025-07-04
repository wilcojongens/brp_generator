# === Snelle instellingen voor niet-programmeurs ===
# Pas hier het aantal dossiers, het aantal bestanden per serie en de leeftijd aan
DEFAULT_AANTAL_DOSSIERS = 10
DEFAULT_AANTAL_BESTANDEN = 1
DEFAULT_LEEFTIJD = 10
BRIN_CODE = "BRIN"
KLAS_OF_GROEP = "groep"
KLASNUMMER = "6"
NAAM_KLAS = ""
ONDERWIJSSOORT = "01"
POSTCODE_RANGE = [7411]

postcode_letters = [("AA", "ZZ")]
straatnamen = [
    "Waldeckstraat", "Pyrmontstraat", "Regentessestraat", "Nassaustraat", "Blekerstraat", "Nieuwstraat",
    "De Regenboog", "Goormaatweg", "IJsselerweg", "Ruwerstraat", "Pathmossingel", "Calicostraat",
    "Janninksweg", "Heidestraat", "Sterkerstraat", "Drukkerstraat"
]
geboorteplaats = [
    "Enschede", "Glanerbrug", "Almelo", "Denekamp", "Borne", "Hengelo", "Markelo", "Holten",
    "Nijverdal", "Oldenzaal", "Rijssen", "Vriezenveen"
]
woonplaatsen = ["Enschede"]

voornamen_man = ["Daan", "Noah", "Jurre", "Ties", "Luuk", "Wessel", "Bas", "Matthijs", "Frank", "Kasper",
                 "Niek", "Joris", "Stijn", "Teun", "Ruud", "Wilco", "Jesse", "Niels", "Tom", "Tim", "Thomas",
                 "Frans", "Stef", "Jos", "Marcel", "Nick", "Arnoud", "Arthur", "Bram", "Christian", "Colin",
                 "Dennis", "Richard", "Edwin", "Eric", "Gavin", "Gilian", "Ingmar"]
voornamen_vrouw = ["Emma", "Mila", "Sophie", "Julia", "Lotte", "Merel", "Rosa", "Lisa", "Rosanne", "Femke",
                   "Annelot", "Jill", "Kirsten", "Naomi", "Lieke", "Jolien", "Veerle", "Floor", "Fleur", "Eline",
                   "Elisa", "Sterre", "Maartje", "Karlijn", "Evelien", "Maaike", "Annika", "Lisanne", "Linda",
                   "Kim", "Kate", "Judith", "Jade", "Ismay", "Ilja", "Hilde", "Danique", "Cisca", "Cindy",
                   "Carla", "Astrid", "Anique", "Anke"]
achternamen = ["Jansen", "Huisman", "Prins", "Visser", "Visscher", "Mertens", "Maas", "Mulder", "Simons",
               "Kuiper", "Kuipers", "Dokter", "Hamer", "Boon", "Evers", "Franken", "Molenaar", "Engels",
               "Bijl", "Verbeke", "Verbeek", "Klaassen", "Arts", "Vis", "Meijer", "Rietveld", "Gorter",
               "Koopmans", "Brummel", "Pen", "Koorn", "Weustink", "Wiggers", "Langeveld", "Huijboom",
               "Govers", "Pol", "Nieveld", "Scholten", " Mentink", "Groot", "Baars", "Prinsze", "Albers",
               "Hartog", "Scherling", "Weijers", "Brink", "Tuitert", "Haspels", "Duzijn", "Tutert", "Klok",
               "Kooij", "Kuyper", "Wilbrink", "Dijkkamp", "Wissink", "Brouwer", "Weverink", "Nengerman",
               "Damhuis", "Bruineberg", "Rijneveen", "Nieskens", "Dollekamp", "Spek", "Bon", "Ruigrok"]


import argparse
import random
import os
import string
from datetime import datetime, timedelta


def generate_random_postcode():
    nummer = str(random.choice(postcode_range))
    while True:
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        for start, end in postcode_letters:
            if start <= letters <= end:
                return f"{nummer}{letters}"


def random_bsn():
    def is_geldig_bsn(bsn_str):
        if len(bsn_str) != 9 or not bsn_str.isdigit():
            return False
        totaal = sum(int(cijfer) * (9 - i) for i, cijfer in enumerate(bsn_str[:8]))
        totaal -= int(bsn_str[8])
        return totaal % 11 == 0

    while True:
        bsn = random.randint(100000000, 999999999)
        if is_geldig_bsn(str(bsn)):
            return str(bsn)


def random_datum():
    huidige_datum = datetime.today()
    start = huidige_datum.replace(year=huidige_datum.year - leeftijd, month=1, day=1)
    end = huidige_datum.replace(year=huidige_datum.year - leeftijd, month=12, day=31)
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).strftime("%Y%m%d")


def generate_record_dict(geslacht):
    voornaam = random.choice(voornamen_man if geslacht == "M" else voornamen_vrouw)
    achternaam = random.choice(achternamen)
    straatnaam = random.choice(straatnamen)
    huisnummer = random.randint(1, 100)
    postcode = generate_random_postcode()
    bsn = random_bsn()
    geboortedatum = args.geboortedatum if args.geboortedatum else random_datum()

    return {
        "bsn": bsn,
        "voornaam": voornaam,
        "achternaam": achternaam,
        "geboortedatum": geboortedatum,
        "straatnaam": straatnaam,
        "huisnummer": huisnummer,
        "postcode": postcode,
        "geslacht": geslacht,
        "geboorteplaats": random.choice(geboorteplaats)
    }


def generate_records(aantal, gebruikte_bsns=None, gebruikte_namen=None):
    if gebruikte_bsns is None:
        gebruikte_bsns = set()
    if gebruikte_namen is None:
        gebruikte_namen = set()
    records = []
    while len(records) < aantal:
        geslacht = random.choice(["M", "V"])
        record = generate_record_dict(geslacht)
        naam = (record["voornaam"], record["achternaam"])
        if record["bsn"] in gebruikte_bsns or naam in gebruikte_namen:
            continue
        gebruikte_bsns.add(record["bsn"])
        gebruikte_namen.add(naam)
        records.append(record)
    return records


def maak_brp_regel(code, inhoud):
    inhoud_schoon = str(inhoud).strip()
    prefix = f"{code}  I"
    inhoud_max_len = 264 - len(prefix)
    if len(inhoud_schoon) > inhoud_max_len:
        raise ValueError(f"Inhoud te lang: {inhoud_schoon}")
    regel = prefix + inhoud_schoon.ljust(inhoud_max_len) + "X"
    return regel


def genereer_a_nummer():
    while True:
        cijfers = [random.randint(0, 9) for _ in range(10)]
        if cijfers[0] == 0:
            continue
        if any(cijfers[i] == cijfers[i + 1] for i in range(9)):
            continue
        som = sum(cijfers)
        if som % 11 not in (0, 5):
            continue
        gewogen_som = sum(c * (2 ** i) for i, c in enumerate(cijfers))
        if gewogen_som % 11 != 0:
            continue
        return ''.join(str(c) for c in cijfers)


def samenstellen_inspoel(records, bestandsnaam="BRP_inspoel.txt"):
    with open(bestandsnaam, "w", encoding="utf-8") as f:
        for r in records:
            a_nummer = genereer_a_nummer()

            a_regel = (
                f"A100000000020200000000126300000000126D4000001261209280330ZAg113000250"
                f"{' ' * 11}{a_nummer}BATCH{' ' * 45}N00000  00000000A00000000{' ' * 13}"
                f"0000{' ' * 10}{r['bsn']}{' ' * 17}00000{' ' * 41}X\n"
            )

            b_regels = [
                maak_brp_regel("B010110", a_nummer),                        # A-nummer
                maak_brp_regel("B010120", r['bsn']),                        # Burgerservicenummer
                maak_brp_regel("B010210", r['voornaam']),                   # Voornamen
                # maak_brp_regel("B01230", )                                  # Voorvoegsel geslachtsnaam
                maak_brp_regel("B010240", r['achternaam']),                 # Geslachtsnaam
                maak_brp_regel("B010310", r['geboortedatum']),              # Geboortedatum
                maak_brp_regel("B010320", r['geboorteplaats']),             # Geboorteplaats
                maak_brp_regel("B010330", "Nederland"),                     # Geboorteland
                maak_brp_regel("B010410", r['geslacht']),                   # Geslachtsaanduiding
                maak_brp_regel("B080910", random.choice(woonplaatsen)),    # Gemeente van inschrijving
                maak_brp_regel("B081110", r['straatnaam']),                 # Straatnaam
                maak_brp_regel("B081120", str(r['huisnummer'])),            # Huisnummer
                maak_brp_regel("B081160", r['postcode'])                    # Postcode
            ]

            f.write(a_regel)
            f.writelines(regel + "\n" for regel in b_regels)


# ONDERWIJSSOORTEN                      ID
#------------------------------------------
# Basisonderwijs                        01
# Basisvorming VMBO/HAVO                02
# Basisvorming HAVO/VWO/Gymnasium       04
# VMBO theoretische leerweg             05
# VMBO overig                           06
# IVBO of VBO                           07
# MAVO                                  08
# Leerlingwezen of KMBO                 09
# HAVO                                  10
# VWO                                   11
# MBO                                   12
# HBO                                   13
# Universiteit                          14
# Speciaal basisonderwijs               15
# Speciaal Boortgezet Onderwijs         16
# REC                                   17
# Praktijkonderwijs                     18
# Geen                                  19
# Anders                                98
# Onbekend                              99

def samenstellen_klassenlijst(records, bestandsnaam="klassenlijst.csv"):
    header = [
        "BRIN-vestigingsnummer", "Klas of groep", "Klas- of groepnummer", "Naam klas", "Onderwijssoort",
        "Zorgpad", "BSN", "Team", "Geboortedatum", "Geslacht", "Achternaam", "Tussenvoegsel",
        "Roepnaam", "Telefoonnummer", "Telefoonnummer 2", "Postcode", "Huisnummer",
        "Voornaam contactpersoon", "Achternaam contactpersoon", "Telefoonnummer contactpersoon",
        "Functie contactpersoon", "Email contactpersoon"
    ]
    with open(bestandsnaam, "w", encoding="utf-8") as f:
        f.write(";".join(header) + "\n")
        for r in records:
            velden = [
                BRIN_CODE,                                                                                  # BRIN-vestigingsnummer
                KLAS_OF_GROEP,                                                                              # Klas of groep
                KLASNUMMER,                                                                                # Klas- of groepnummer
                NAAM_KLAS,                                                                                 # Naam klas
                ONDERWIJSSOORT,                                                                            # Onderwijssoort
                "",                                                                                        # Zorgpad
                r['bsn'],                                                                                  # BSN
                "",                                                                                        # Team
                f"{r['geboortedatum'][6:8]}-{r['geboortedatum'][4:6]}-{r['geboortedatum'][:4]}",           # Geboortedatum
                r['geslacht'],                                                                             # Geslacht
                r['achternaam'],                                                                           # Achternaam
                "",                                                                                        # Tussenvoegsel
                r['voornaam'],                                                                             # Roepnaam
                "",                                                                                        # Telefoonnummer
                "",                                                                                        # Telefoonnummer 2
                r['postcode'],                                                                             # Postcode
                "",                                                                                        # Huisnummer
                "",                                                                                        # Voornaam contactpersoon
                "",                                                                                        # Achternaam contactpersoon
                "",                                                                                        # Telefoonnummer contactpersoon
                "",                                                                                        # Functie contactpersoon
                ""                                                                                         # Email contactpersoon
            ]
            f.write(";".join(velden) + "\n")


def genereer_unieke_mapnaam(prefix="BRP_serie_", basispad="../output"):
    teller = 1
    while True:
        mapnaam = os.path.join(basispad, f"{prefix}{teller}")
        if not os.path.exists(mapnaam):
            os.makedirs(mapnaam)
            return mapnaam
        teller += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--aantal_dossiers", type=int, default=DEFAULT_AANTAL_DOSSIERS,
                        help="Aantal dossiers per bestand")
    parser.add_argument("--aantal_bestanden", type=int, default=DEFAULT_AANTAL_BESTANDEN,
                        help="Aantal bestanden per serie")
    parser.add_argument("--leeftijd", type=int, default=DEFAULT_LEEFTIJD,
                        help="Leeftijd van de gegenereerde personen")
    parser.add_argument("--geboortedatum", type=str,
                        help="Specifieke geboortedatum in YYYYMMDD formaat, laat leeg om te genereren op basis van leeftijd")
    parser.add_argument("--brin", type=str, default=BRIN_CODE,
                        help="BRIN-code van de school")
    parser.add_argument("--klas_of_groep", type=str, default=KLAS_OF_GROEP,
                        help="Klas of groep aanduiding")
    parser.add_argument("--klasnummer", type=str, default=KLASNUMMER,
                        help="Klas- of groepsnummer")
    parser.add_argument("--naam_klas", type=str, default=NAAM_KLAS,
                        help="Naam van de klas")
    parser.add_argument("--onderwijssoort", type=str, default=ONDERWIJSSOORT,
                        help="Onderwijssoortcode (bijv. 01 voor basisonderwijs)")

    parser.add_argument("--postcode_range", nargs="+", type=int, default=POSTCODE_RANGE,
                        help="Lijst van numerieke postcodes (bv. 7411 7412 7413)")
    args = parser.parse_args()

    aantal_dossiers = args.aantal_dossiers
    aantal_bestanden = args.aantal_bestanden
    leeftijd = args.leeftijd
    BRIN_CODE = args.brin
    KLAS_OF_GROEP = args.klas_of_groep
    KLASNUMMER = args.klasnummer
    NAAM_KLAS = args.naam_klas
    ONDERWIJSSOORT = args.onderwijssoort
    postcode_range = args.postcode_range


    outputmap = genereer_unieke_mapnaam()
    gebruikte_bsns = set()
    gebruikte_namen = set()
    for i in range(1, aantal_bestanden + 1):
        leerlingen = generate_records(aantal_dossiers, gebruikte_bsns, gebruikte_namen)
        submap = os.path.join(outputmap, f"set_{i}")
        os.makedirs(submap, exist_ok=True)
        inspoel_pad = os.path.join(submap, f"BRP_inspoel_{i}.txt")
        klassenlijst_pad = os.path.join(submap, f"klassenlijst_{i}.csv")
        samenstellen_inspoel(leerlingen, bestandsnaam=inspoel_pad)
        samenstellen_klassenlijst(leerlingen, bestandsnaam=klassenlijst_pad)