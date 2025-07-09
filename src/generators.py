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


def random_datum(leeftijd):
    huidige_datum = datetime.today()
    start = huidige_datum.replace(year=huidige_datum.year - leeftijd, month=1, day=1)
    end = huidige_datum.replace(year=huidige_datum.year - leeftijd, month=12, day=31)
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).date()