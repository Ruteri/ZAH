# Punkty do odwiedzenia i łączące je drogi
set PUNKTY;
set DROGI within (PUNKTY) cross (PUNKTY);
param N := 6 ;

# Punkt początkowy i odległości (długości dróg)
param PIEKARNIA symbolic in PUNKTY;
param ODLEGLOSC {DROGI} >= 0;

# Tablica określająca przynależność drogi do wybranej trasy
var UZYCIE_DROGI {(i,j) in DROGI} integer >= 0, <= 1;
var KROK_ODWIEDZENIA {PUNKTY} >= 0 integer ;
minimize FUNKCJA_CELU: sum {(i,j) in DROGI} ODLEGLOSC[i,j] * UZYCIE_DROGI[i,j];

# Zapewnia, że przyjeżdżamy do każdego punktu
subject to KONIECZNOSC_ODWIEDZENIA {i in PUNKTY}:
sum {(i,j) in DROGI} UZYCIE_DROGI[i,j] = 1;

# Zapewnia, że wyjeżdżamy z każdego punktu
subject to KONIECZNOSC_OPUSZCZENIA {j in PUNKTY}:
sum {(i,j) in DROGI} UZYCIE_DROGI[i,j] = 1;

#ZAPEWNIA ZE MAMY TYLKO JEDEN CYKL
subject to JEDEN_CYKL{k in PUNKTY, j in PUNKTY: j > 1 and k > 1}:  
           KROK_ODWIEDZENIA[j] - KROK_ODWIEDZENIA[k] + N*UZYCIE_DROGI[j,k] <= N-1;

# Zapewnia, że każda droga użyta jest tylko raz
subject to SPOJNOSC {(i,j) in DROGI}:
UZYCIE_DROGI[i,j] + UZYCIE_DROGI[j,i] <= 1;