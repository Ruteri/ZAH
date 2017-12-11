

set punkty;
set kierowcy ;
set pieczywa ;
var U{kierowcy,punkty} >= 0 integer;
param DROGI{punkty, punkty} >= 0;
var SPRZEDAZ{punkty,kierowcy,pieczywa} >= 0 integer;
var NIEZADOWOLENIE { punkty, pieczywa} >= 0 integer;
var UZYCIE_DROGI{kierowcy,punkty,punkty} binary;
param N := card(punkty);
param P := card(pieczywa);
param K := card(kierowcy);

param miasta{punkty} symbolic;
param imie{kierowcy} symbolic;
param typy{pieczywa} symbolic;
var UZYCIE_KIEROWCY{kierowcy} ;
param POPYT {punkty,pieczywa} >= 0;
param CENA {punkty,pieczywa} >= 0;
param WAGA_NIEZADOWOLENIA {punkty,pieczywa } >= 0;
param PODAZ{pieczywa};
param KOSZT_KIEROWCY{kierowcy} ;  # kosz kierowcy za km 
param POJEMNOSC{kierowcy} ;
param OBJETOSC{pieczywa} ;
var ZABRANE{kierowcy,pieczywa} ;

# Sprzedaż w danym punkcie




        
maximize FUNKCJA_CELU: sum {p in pieczywa,i in punkty,d in kierowcy } SPRZEDAZ[i,d,p] * CENA[i,p] - sum {i in punkty ,p in pieczywa}  WAGA_NIEZADOWOLENIA[i,p] * NIEZADOWOLENIE[i,p] -sum{d in kierowcy ,i in punkty, j in punkty}KOSZT_KIEROWCY[d]* DROGI[i,j]*UZYCIE_DROGI[d,i,j];
subject to 
       
        c1{k in punkty:k>1}: sum{i in punkty,d in kierowcy} UZYCIE_DROGI[d,i,k] = 1;       
        c2{k in punkty:k>1}: sum{j in punkty,d in kierowcy} UZYCIE_DROGI[d,k,j] = 1;         
        c11 {d in kierowcy,i in punkty: i<2}: sum { j in punkty} UZYCIE_DROGI[d,i,j]=1 ; # -(1-UZYCIE_KIEROWCY[d]) ;  z tym optymalizujemy ilośc kierowcow ale poki co to nie ma sensu  
        c21 {d in kierowcy,i in punkty: i<2}: sum { j in punkty} UZYCIE_DROGI[d,j,i]=1 ; #-(1-UZYCIE_KIEROWCY[d]) ;  # dopki nie ma nagrody za szybkość
        c111{d in kierowcy,j in punkty}: sum {i in punkty}  UZYCIE_DROGI[d,j,i]=sum {i in punkty}  UZYCIE_DROGI[d,i,j] ;
        c3{d in kierowcy ,k in punkty, j in punkty: j > 1 and k > 1}:  
           U[d,j] - U[d,k] + N*UZYCIE_DROGI[d,j,k] <= N-1;
       
        c4 {i in punkty,p in pieczywa}: sum{k in kierowcy}SPRZEDAZ[i,k,p] <= POPYT[i,p];
        c5 {i in punkty,p in pieczywa}: NIEZADOWOLENIE[i,p] = POPYT[i,p] - sum{k in kierowcy}SPRZEDAZ[i,k,p];  
        c8 {d in kierowcy}: sum{p in pieczywa}ZABRANE[d,p]* OBJETOSC[p] <= POJEMNOSC[d]  ;
        c9 {d in kierowcy , p in pieczywa}: sum{i in punkty }SPRZEDAZ[i,d,p] <= ZABRANE[d,p] ;
        c6{p in pieczywa}: sum {k in kierowcy} ZABRANE[k,p] <= PODAZ[p];
        
                   
          


 






data;



param POPYT : 1   2   3 :=
1             100 100 100
2             100 100 100
3             100 100 100
4             100 100 100  
5             100 100 100 ;

param CENA:  1   2   3 :=
1             2 2 2
2             2 2 2
3             2 2 2
4             2 2 2  
5             2 2 2 ;

param WAGA_NIEZADOWOLENIA:  1   2   3 :=
1             0.2 0.2 0.2
2             0.2 0.2 0.2
3             0.2 0.2 0.2
4             0.2 0.2 0.2  
5             0.2 0.2 0.2 ;


param: kierowcy: imie := 
 1 "Janusz"
 2 "Andrzej"
 3 "Blacha"
  ;
  
param: pieczywa: typy := 
1 "Jasne"  
2 "Ciemne"  
3 "Prawilne"
  ;
  
 param:  PODAZ := 
 1 300 
 2 150  
 3 400
  ;
 param: OBJETOSC:=
 1 1
 2 2
 3 1 
 ;
  param: POJEMNOSC:=
 1 200
 2 200
 3 300 
 ;
 
param:  KOSZT_KIEROWCY := 
 1 1
 2 1
 3 1
  ;

param: punkty: miasta := 
        1 "Piekarnia"
        2 "A"
        3 "B"
        4 "C"
        5 "D"
;


param DROGI: 1 2 3 4 5 :=
        1 50000 732 217 564 58
        2 217 50000 290 201 79
        3 217 290 50000 113 303
        4 164 201 113 50000 196
        5 58 89 403 196 50000
;