#include "Beispielvertrag.h"
int main(void) {
    const char Daten[]="C Datei: de 😀\n";
    int Datei=dateiÖffnen("c.txt",LesenSchreiben|ErstellenFallsFehlend|KürzenInhalt,0600);
    if(Datei<0)return 1;
    if(dateiDatenSchreiben(Datei,Daten,sizeof(Daten)-1)!=sizeof(Daten)-1)return 2;
    if(dateiPositionieren(Datei,0,VonAnfang)!=0)return 3;
    char textWertLesen[128]={0};int Länge=dateiDatenLesen(Datei,textWertLesen,sizeof(textWertLesen)-1);
    dateiSchließen(Datei);
    if(Länge!=sizeof(Daten)-1)return 4;
    for(int Zahl=0;Zahl<Länge;Zahl++)if(Daten[Zahl]!=textWertLesen[Zahl])return 5;
    return Ausgabe(textWertLesen);
}
