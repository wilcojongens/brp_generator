from generators import genereer_unieke_mapnaam, random_bsn
from generateBrp import samenstellen_inspoel
from generateKlassenlijst import samenstellen_klassenlijst, schoolRecord
from record import generateMultipleRecords
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--aantal_dossiers", type=int,
                        help="Aantal dossiers per bestand")
    parser.add_argument("--aantal_bestanden", type=int,
                        help="Aantal bestanden per serie")
    parser.add_argument("--leeftijd", type=int,
                        help="Leeftijd van de gegenereerde personen")
    parser.add_argument("--brin", type=str,
                        help="BRIN-code van de school")
    parser.add_argument("--klas_of_groep", type=str,
                        help="Klas of groep aanduiding")
    parser.add_argument("--klasnummer", type=str,
                        help="Klas- of groepsnummer")
    parser.add_argument("--naam_klas", type=str,
                        help="Naam van de klas")
    parser.add_argument("--onderwijssoort", type=str,
                        help="Onderwijssoortcode (bijv. 01 voor basisonderwijs)")
    parser.add_argument("--postcode_range", nargs="+", type=int,
                        help="Lijst van numerieke postcodes (bv. 7411 7412 7413)")
    parser.add_argument("--geboortedatum", type=str,
                        help="Specifieke geboortedatum in YYYYMMDD formaat, laat leeg om te genereren op basis van leeftijd")
    parser.add_argument("--achternaam", type=str,
                        help="Achternaam van de gegenereerde personen")
    parser.add_argument("--naamvader", type=str,
                        help="Voornaam van de vader van de gegenereerde personen")
    parser.add_argument("--fixbsnvader", action="store_true",
                        help="BSN van de vader van de gegenereerde personen wordt gefixeerd voor alle dossiers")
    parser.add_argument("--naammoeder", type=str,
                        help="Voornaam van de moeder van de gegenereerde personen")
    parser.add_argument("--fixbsnmoeder", action="store_true",
                        help="BSN van de moeder van de gegenereerde personen wordt gefixeerd voor alle dossiers")
    parser.add_argument("--adres", type=str,
                        help="Adres van de gegenereerde personen (bv. 'Waldeckstraat 1 7411AA Deventer')")
    args = parser.parse_args()

    schoolRecord = schoolRecord(
        brinCode=args.brin,
        klasOfGroep=args.klas_of_groep,
        klasnummer=args.klasnummer,
        naamKlas=args.naam_klas,
        onderwijssoort=args.onderwijssoort
    )

    # Genereer fixed BSN's als opgegeven
    fixed_bsn_vader = None
    fixed_bsn_moeder = None
    
    if args.fixbsnvader:
        fixed_bsn_vader = random_bsn()
        print(f"Fixed BSN voor vader gegenereerd: {fixed_bsn_vader}")
    
    if args.fixbsnmoeder:
        fixed_bsn_moeder = random_bsn()
        print(f"Fixed BSN voor moeder gegenereerd: {fixed_bsn_moeder}")

    outputmap = genereer_unieke_mapnaam()
    gebruikte_bsns = set()
    gebruikte_namen = set()
    aantal_bestanden = args.aantal_bestanden if args.aantal_bestanden is not None else 1
    for i in range(1, aantal_bestanden + 1):
        leerlingen = generateMultipleRecords(
            args,
            (args.aantal_dossiers or 10),
            gebruikte_bsns,
            gebruikte_namen,
            fixed_bsn_vader,
            fixed_bsn_moeder
        )
        submap = os.path.join(outputmap, f"set_{i}")
        os.makedirs(submap, exist_ok=True)
        inspoel_pad = os.path.join(submap, f"BRP_inspoel_{i}.txt")
        klassenlijst_pad = os.path.join(submap, f"klassenlijst_{i}.csv")
        samenstellen_inspoel(leerlingen, bestandsnaam=inspoel_pad)
        samenstellen_klassenlijst(leerlingen, schoolRecord, bestandsnaam=klassenlijst_pad)