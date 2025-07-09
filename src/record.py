from data.namen import voornamen_man, voornamen_vrouw, achternamen
from generators import random_bsn, random_datum, generate_random_postcode
from data.adressen import straatnamen, plaatsnamen
from dataclasses import dataclass
import datetime
import random

@dataclass
class Record:
    bsn: str
    voornaamKind: str
    achternaam: str
    geboortedatum: datetime.date
    straatnaam: str
    huisnummer: int
    postcode: str
    woonplaats: str
    geslacht: str
    geboorteplaats: str
    voornaamVader: str
    bsnVader: str
    voornaamMoeder: str
    bsnMoeder: str

def generateSingleRecord(args, geslacht, fixed_bsn_vader=None, fixed_bsn_moeder=None):
    voornaam = random.choice(voornamen_man if geslacht == "M" else voornamen_vrouw)
    achternaam = getattr(args, "achternaam", None) or random.choice(achternamen)
    geboortedatum = getattr(args, "geboortedatum", None) or random_datum(args.leeftijd or 10)

    # Genereer voornamen voor ouders
    voornaam_vader = getattr(args, "naamvader", None) or random.choice(voornamen_man)
    voornaam_moeder = getattr(args, "naammoeder", None) or random.choice(voornamen_vrouw)

    # Gebruik fixed BSN's als opgegeven, anders genereer nieuwe
    bsn_vader = fixed_bsn_vader if fixed_bsn_vader else random_bsn()
    bsn_moeder = fixed_bsn_moeder if fixed_bsn_moeder else random_bsn()

    if getattr(args, "adres", None):
        straatnaam, huisnummer, postcode, woonplaats = args.adres.split(" ")
    else:
        straatnaam = random.choice(straatnamen)
        huisnummer = random.randint(1, 100)
        postcode = generate_random_postcode()
        woonplaats = random.choice(plaatsnamen)

    return Record(
        bsn=random_bsn(),
        voornaamKind=voornaam,
        achternaam=achternaam,
        geboortedatum=geboortedatum,
        straatnaam=straatnaam,
        huisnummer=huisnummer,
        postcode=postcode,
        woonplaats=woonplaats,
        geslacht=geslacht,
        geboorteplaats=random.choice(plaatsnamen),
        voornaamVader=voornaam_vader,
        bsnVader=bsn_vader,
        voornaamMoeder=voornaam_moeder,
        bsnMoeder=bsn_moeder
    )

def generateMultipleRecords(args, aantal, gebruikte_bsns=None, gebruikte_namen=None, fixed_bsn_vader=None, fixed_bsn_moeder=None):
    if gebruikte_bsns is None:
        gebruikte_bsns = set()
    if gebruikte_namen is None:
        gebruikte_namen = set()
    
    # Voeg fixed BSN's toe aan gebruikte BSN's (als ze bestaan)
    if fixed_bsn_vader:
        gebruikte_bsns.add(fixed_bsn_vader)
    if fixed_bsn_moeder:
        gebruikte_bsns.add(fixed_bsn_moeder)
    
    records = []
    while len(records) < aantal:
        geslacht = random.choice(["M", "V"])
        record = generateSingleRecord(args, geslacht, fixed_bsn_vader, fixed_bsn_moeder)
        naam = (record.voornaamKind, record.achternaam)
        
        # Controleer of BSN's uniek zijn (alleen het kind-BSN hoeft uniek te zijn als ouder-BSN's gefixed zijn)
        if fixed_bsn_vader and fixed_bsn_moeder:
            # Beide ouder-BSN's zijn gefixed, alleen kind-BSN moet uniek zijn
            if record.bsn in gebruikte_bsns or naam in gebruikte_namen:
                continue
        elif fixed_bsn_vader:
            # Alleen vader-BSN is gefixed
            bsns_in_record = {record.bsn, record.bsnMoeder}
            if (record.bsn in gebruikte_bsns or 
                record.bsnMoeder in gebruikte_bsns or
                naam in gebruikte_namen or
                len(bsns_in_record) < 2):
                continue
        elif fixed_bsn_moeder:
            # Alleen moeder-BSN is gefixed
            bsns_in_record = {record.bsn, record.bsnVader}
            if (record.bsn in gebruikte_bsns or 
                record.bsnVader in gebruikte_bsns or
                naam in gebruikte_namen or
                len(bsns_in_record) < 2):
                continue
        else:
            # Geen fixed BSN's, alle BSN's moeten uniek zijn
            bsns_in_record = {record.bsn, record.bsnVader, record.bsnMoeder}
            if (record.bsn in gebruikte_bsns or 
                record.bsnVader in gebruikte_bsns or 
                record.bsnMoeder in gebruikte_bsns or
                naam in gebruikte_namen or
                len(bsns_in_record) < 3):
                continue
        
        # Voeg alleen nieuwe BSN's toe aan gebruikte set
        gebruikte_bsns.add(record.bsn)
        if not fixed_bsn_vader:
            gebruikte_bsns.add(record.bsnVader)
        if not fixed_bsn_moeder:
            gebruikte_bsns.add(record.bsnMoeder)
        gebruikte_namen.add(naam)
        records.append(record)
    return records

