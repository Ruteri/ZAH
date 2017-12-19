

set punkty;
set pieczywa ;
var U{punkty} >= 0 integer;
param DROGI{punkty, punkty} >= 0;
var SPRZEDAZ{punkty,pieczywa} >= 0 integer;
var NIEZADOWOLENIE { punkty, pieczywa} >= 0 integer;
var UZYCIE_DROGI{punkty,punkty} binary;
param N := card(punkty);
param P := card(pieczywa);
param A := 7000 ;

param miasta{punkty} symbolic;
param typy{pieczywa} symbolic;
param POPYT {punkty,pieczywa} >= 0;
param CENA {punkty,pieczywa} >= 0;
param WAGA_NIEZADOWOLENIA {punkty,pieczywa } >= 0;
param PODAZ{pieczywa};
param KOSZT_KIEROWCY;  # kosz kierowcy za km 
param POJEMNOSC;
param OBJETOSC{pieczywa} ;
var ZABRANE{pieczywa} ;
var z{i in punkty} >= 0 ;

# Sprzedaż w danym punkcie




        
maximize FUNKCJA_CELU: sum {p in pieczywa,i in punkty} SPRZEDAZ[i,p] * CENA[i,p] - sum {i in punkty ,p in pieczywa}  WAGA_NIEZADOWOLENIA[i,p] * NIEZADOWOLENIE[i,p] -sum{i in punkty, j in punkty}KOSZT_KIEROWCY* DROGI[i,j]*UZYCIE_DROGI[i,j];
subject to 
       
        c1{k in punkty:k>1}: sum{i in punkty} UZYCIE_DROGI[i,k] = 1;       
        c2{k in punkty:k>1}: sum{j in punkty} UZYCIE_DROGI[k,j] = 1;         
        c11 {i in punkty: i<2}: sum { j in punkty} UZYCIE_DROGI[i,j]=1 ;
        c21 {i in punkty: i<2}: sum { j in punkty} UZYCIE_DROGI[j,i]=1 ;
        c111{j in punkty}: sum {i in punkty}  UZYCIE_DROGI[j,i]=sum {i in punkty}  UZYCIE_DROGI[i,j] ;
        c3{k in punkty, j in punkty: j > 1 and k > 1}:  
           U[j] - U[k] + N*UZYCIE_DROGI[j,k] <= N-1;
       
        c4 {i in punkty,p in pieczywa}: SPRZEDAZ[i,p] <= POPYT[i,p];
        c5 {i in punkty,p in pieczywa}: NIEZADOWOLENIE[i,p] = POPYT[i,p] - SPRZEDAZ[i,p];  
        c8: sum{p in pieczywa}ZABRANE[p]* OBJETOSC[p] <= POJEMNOSC  ;
        c9 {p in pieczywa}: sum{i in punkty }SPRZEDAZ[i,p] <= ZABRANE[p] ;
        c6{p in pieczywa}: ZABRANE[p] <= PODAZ[p];
        c10{i in punkty }: sum{p in pieczywa}SPRZEDAZ[i,p] <= z[i] ; #sum { k in punkty}UZYCIE_DROGI[d,k,i]*sum{p in pieczywa}SPRZEDAZ[i,d,p]
        z1{i in punkty} : z[i] <= A* sum { k in punkty}UZYCIE_DROGI[k,i] ;
        z2 {i in punkty}: z[i] <= sum{p in pieczywa}SPRZEDAZ[i,p] ;
        z3 {i in punkty}: z[i] >=  sum{p in pieczywa}SPRZEDAZ[i,p] - (1-sum { k in punkty}UZYCIE_DROGI[k,i])*A ;    
          
data;
  
param: pieczywa: typy := 
1 "Jasne"  
2 "Ciemne"  
3 "Prawilne"
  ;

param: punkty: miasta := 
        1 "Piekarnia"
        2 "A"
        3 "B"
        4 "C"
        5 "D"
;