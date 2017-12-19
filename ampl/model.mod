set PUNKTY;
set PIECZYWA ;
param drogi{PUNKTY, PUNKTY} >= 0;
param N := card(PUNKTY);
param P := card(PIECZYWA);
param A := 7000 ;
param miasta{PUNKTY} symbolic;
param typy{PIECZYWA} symbolic;
param popyt {PUNKTY,PIECZYWA} >= 0;
param cena {PUNKTY,PIECZYWA} >= 0;
param podaz{PIECZYWA};
param koszt_kierowcy;  # kosz kierowcy za km 
param pojemnosc;
param objetosc{PIECZYWA} ;
var Zabrane{PIECZYWA} ;
var z{i in PUNKTY} >= 0 ;
var Sprzedaz{PUNKTY,PIECZYWA} >= 0 integer;
var Uzycie_drogi{PUNKTY,PUNKTY} binary;
var Krok_odwiedzenia{PUNKTY} >= 0 integer;





        
maximize FUNKCJA_CELU: sum {p in PIECZYWA,i in PUNKTY} Sprzedaz[i,p] * cena[i,p]  -sum{i in PUNKTY, j in PUNKTY}koszt_kierowcy* drogi[i,j]*Uzycie_drogi[i,j];
subject to 
       
        c1{k in PUNKTY:k>1}: sum{i in PUNKTY} Uzycie_drogi[i,k] = 1;       
        c2{k in PUNKTY:k>1}: sum{j in PUNKTY} Uzycie_drogi[k,j] = 1;         
        c11 {i in PUNKTY: i<2}: sum { j in PUNKTY} Uzycie_drogi[i,j]=1 ;
        c21 {i in PUNKTY: i<2}: sum { j in PUNKTY} Uzycie_drogi[j,i]=1 ;
        c111{j in PUNKTY}: sum {i in PUNKTY}  Uzycie_drogi[j,i]=sum {i in PUNKTY}  Uzycie_drogi[i,j] ;
        c3{k in PUNKTY, j in PUNKTY: j > 1 and k > 1}:  
           Krok_odwiedzenia[j] - Krok_odwiedzenia[k] + N*Uzycie_drogi[j,k] <= N-1;
       
        c4 {i in PUNKTY,p in PIECZYWA}: Sprzedaz[i,p] <= popyt[i,p];
        
        c8: sum{p in PIECZYWA}Zabrane[p]* objetosc[p] <= pojemnosc  ;
        c9 {p in PIECZYWA}: sum{i in PUNKTY }Sprzedaz[i,p] <= Zabrane[p] ;
        c6{p in PIECZYWA}: Zabrane[p] <= podaz[p];
        c10{i in PUNKTY }: sum{p in PIECZYWA}Sprzedaz[i,p] <= z[i] ; #sum { k in PUNKTY}Uzycie_drogi[d,k,i]*sum{p in PIECZYWA}Sprzedaz[i,d,p]
        z1{i in PUNKTY} : z[i] <= A* sum { k in PUNKTY}Uzycie_drogi[k,i] ;
        z2 {i in PUNKTY}: z[i] <= sum{p in PIECZYWA}Sprzedaz[i,p] ;
        z3 {i in PUNKTY}: z[i] >=  sum{p in PIECZYWA}Sprzedaz[i,p] - (1-sum { k in PUNKTY}Uzycie_drogi[k,i])*A ;    
          
data;



param popyt : 1   2   3 :=
1             000 000 000
2             100 100 100
3             100 100 100
4             100 100 100  
5             100 100 100 ;

param cena:  1   2   3 :=
1             2 2 2
2             2 2 2
3             2 2 2
4             2 2 2  
5             2 2 2 ;


  
param: PIECZYWA: typy := 
1 "Jasne"  
2 "Ciemne"  
3 "Prawilne"
  ;
  
 param:  podaz := 
 1 300 
 2 150  
 3 400
  ;
 param: objetosc:=
 1 1
 2 2
 3 1 
 ;
  param pojemnosc:= 200;
 
param  koszt_kierowcy := 1;

param: PUNKTY: miasta := 
        1 "Piekarnia"
        2 "A"
        3 "B"
        4 "C"
        5 "D"
;


param drogi: 1 2 3 4 5 :=
        1 50000 732 217 564 58
        2 217 50000 290 201 79
        3 217 290 50000 113 303
        4 164 201 113 50000 196
        5 58 89 403 196 50000
;