from data.adressen import postcode_letters, postcode_range
from datetime import datetime, timedelta
import random
import string
import os

def genereer_unieke_mapnaam(prefix="BRP_serie_", basispad="../output"):
    teller = 1
    while True:
        mapnaam = os.path.join(basispad, f"{prefix}{teller}")
        if not os.path.exists(mapnaam):
            os.makedirs(mapnaam)
            return mapnaam
        teller += 1


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


def random_datum(minimum_leeftijd, maximum_leeftijd=None):
    """
    Genereert een willekeurige geboortedatum tussen minimum en maximum leeftijd.
    
    Args:
        minimum_leeftijd (int): Minimale leeftijd in jaren
        maximum_leeftijd (int, optional): Maximale leeftijd in jaren. 
                                        Als niet opgegeven, wordt minimum_leeftijd als maximum gebruikt.
    
    Returns:
        datetime.date: Geboortedatum die resulteert in een leeftijd tussen min en max
    """
    if maximum_leeftijd is None:
        maximum_leeftijd = minimum_leeftijd
    
    if minimum_leeftijd > maximum_leeftijd:
        raise ValueError("Minimum leeftijd kan niet groter zijn dan maximum leeftijd")
    
    huidige_datum = datetime.today()
    
    # Bereken de datum ranges die resulteren in de gewenste leeftijden
    # Voor minimum leeftijd: kind moet minstens X jaar oud zijn
    max_geboortedatum = huidige_datum.replace(year=huidige_datum.year - minimum_leeftijd, month=huidige_datum.month, day=huidige_datum.day)
    
    # Voor maximum leeftijd: kind mag maximaal Y jaar oud zijn  
    min_geboortedatum = huidige_datum.replace(year=huidige_datum.year - maximum_leeftijd - 1, month=huidige_datum.month, day=huidige_datum.day) + timedelta(days=1)
    
    # Genereer willekeurige datum tussen deze grenzen
    delta = (max_geboortedatum - min_geboortedatum).days
    if delta < 0:
        raise ValueError(f"Geen geldige datumrange mogelijk voor leeftijden {minimum_leeftijd}-{maximum_leeftijd}")
    
    random_date = min_geboortedatum + timedelta(days=random.randint(0, delta))
    
    # Valideer dat de gegenereerde datum resulteert in de juiste leeftijd
    leeftijd = (huidige_datum - random_date).days // 365
    if leeftijd < minimum_leeftijd or leeftijd > maximum_leeftijd:
        # Als validatie faalt, probeer het opnieuw (recursief)
        return random_datum(minimum_leeftijd, maximum_leeftijd)
    
    return random_date.date()