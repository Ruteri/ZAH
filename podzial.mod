set PUNKTY;

param POPYT {PUNKTY} >= 0;
param CENA {PUNKTY} >= 0;
param WAGA_NIEZADOWOLENIA {PUNKTY} >= 0;
param PODAZ;

# Sprzedaż w danym punkcie
var SPRZEDAZ {i in PUNKTY} >= 0;
var NIEZADOWOLENIE {i in PUNKTY} >= 0;

maximize FUNKCJA_CELU: sum {i in PUNKTY} SPRZEDAZ[i] * CENA[i] - sum {i in PUNKTY} WAGA_NIEZADOWOLENIA[i] * NIEZADOWOLENIE[i];

# Ograniczenia wynikające z popytu i podaży
subject to OGR_PODAZY: sum {i in PUNKTY} SPRZEDAZ[i] = PODAZ;
subject to OGR_POPYTU {i in PUNKTY}: SPRZEDAZ[i] <= POPYT[i];

# Definicja niezadowolenia
subject to OGR_NIEZADOWOLENIA {i in PUNKTY}: NIEZADOWOLENIE[i] = POPYT[i] - SPRZEDAZ[i];