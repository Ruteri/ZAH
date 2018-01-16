# Punkty do odwiedzenia i łączące je drogi
set PUNKTY;
set DROGI within (PUNKTY) cross (PUNKTY);

# Punkt początkowy i odległości (długości dróg)
param PIEKARNIA symbolic in PUNKTY;
param ODLEGLOSC {DROGI} >= 0;

# Tablica określająca przynależność drogi do wybranej trasy
var UZYCIE_DROGI {(i,j) in DROGI} integer >= 0, <= 1;

minimize FUNKCJA_CELU: sum {(i,j) in DROGI} ODLEGLOSC[i,j] * UZYCIE_DROGI[i,j];

#subject to Total: sum {(PIEKARNIA,j) in DROGI} UZYCIE_DROGI[PIEKARNIA,j] = 2;

# Zapewnia, że wszystkie punkty są odwiedzone
subject to KONIECZNOSC_ODWIEDZENIA {i in PUNKTY}:
sum {(i,j) in DROGI} UZYCIE_DROGI[i,j] >= 2;

# Zapewnia spójność (symetryczność) UZYCIE_TABLICY
subject to SPOJNOSC {(i,j) in DROGI}:
UZYCIE_DROGI[i,j] = UZYCIE_DROGI[j,i]