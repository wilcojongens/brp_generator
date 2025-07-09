# brp_generator

## Optionele arguments;

--aantal_dossiers
Bepaald het aantal dossiers wat gegenereerd wordt
Default: 10

--aantal_bestanden
Bepaald het aantal bestanden waarin de dossiers worden opgenomen
Default: 1

--leeftijd
Leeftijd van de te genereren personen, er wordt een willekeurige datum gekozen van X jaar geleden
Default: 10

--brin
Brin van de school waar de kinderen in worden geplaatst
Default: BRIN

--klas_of_groep
Of het een klas of groep is waarin de kinderen worden geplaatst
Default: Groep

--klasnummer
Nummer van de klas of groep waarin de kinderen worden geplaatst
Default: 6

--naam_klas
Naam van de klas of groep waarin de kinderen worden geplaatst
Default: Leeg

--onderwijssoort
Onderwijssoort voor de klas of groep waarin de kinderen worden geplaatst
Op basis van de BDS onderwijssoorten.
Default: 01

--postcode_range
Postcode range die gebruikt dient te worden
Default: [7411]

## Override arguments

--geboortedatum
Override om een specifieke geboortedatum te hanteren voor alle dossiers
Format: YYYYMMDD

--achternaam
Override om een specifieke achternaam te hanteren voor alle dossiers

--naamvader
Override om een specifieke voornaam voor de vader te hanteren voor alle dossiers

--fixbsnvader
Override om een specifiek BSN voor de vader te hanteren voor alle dossiers

--naammoeder
--Override om een specifieke voornaam voor de moeder te hanteren voor alle dossiers

--fixbsnmoeder
Override om een specifiek BSN voor de moeder te hanteren voor alle dossiers

--adres
Override om een specifiek adres te hanteren voor alle dossiers
Format: "Straatnaam 1 1234AA Plaats"
