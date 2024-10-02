# Stregliste
Program, der genererer streglister til de mange hytteture og revybegivenheder på fysikstudiet ogdownload resten af Nørre Campus på Københavns Universitet.

## Afhængigheder
Dette program kræver ```Python 3``` og ```pdflatex``` installeret og tilgængelig i PATH.

## Brug
Programmet køres i terminalen sammen med en CSV-fil, der indeholder kolonnerne "First name" og "Last name". Programmet antager filnavnet "participants.csv", men alternative filnavne kan tilføjes som vist nedenunder.

```python stregliste.py -f deltagere.csv```

Herefter genereres en stregliste.
Der kan laves egne kolonner til streglisten ved flaget ```-h```, der tager en semikolonsepareret streng med kolonnenavne. F.eks.

```python stregliste.py -h "Vand;Sodavand;Toast"```

For en hjælpemenu, kør ```python stregliste.py --help```.
