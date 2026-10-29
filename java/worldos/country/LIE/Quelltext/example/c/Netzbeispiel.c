#include "Beispielvertrag.h"
#include <NetzwerkABI.h>
int main(int argumentAnzahl,char **argumente) {
    if(argumentAnzahl!=2)return Ausgabe("사용법: ./네트워크 UDP창구번호\n");
    unsigned portWert=0;for(int Zahl=0;argumente[1][Zahl];Zahl++) {
        if(argumente[1][Zahl]<'0'||argumente[1][Zahl]>'9')return 2;
        portWert=portWert*10+argumente[1][Zahl]-'0';if(portWert>65535)return 2;
    }
    if(!portWert)return 2;
    int endpunkt=endpunktErstellen(InternetFamilie,DatagrammNetzbuchse,DatagrammProtokoll);if(endpunkt<0)return 3;
    struct InternetNetzbuchseAdresse adresse={0};adresse.adresseFamilie=InternetFamilie;
    if(adresseZuordnen(endpunkt,(struct NetzbuchseAdresse *)&adresse,sizeof(adresse))<0)return 4;
    adresse.portNummer=netzwerkKurz(portWert);adresse.InternetAdresse.adresseWert=netzwerkGanzzahl(0x0a000202);
    const char datagramm[]="C UDP Deutsch";
    if(datagrammDatenSenden(endpunkt,datagramm,sizeof(datagramm)-1,0,(struct NetzbuchseAdresse *)&adresse,sizeof(adresse))!=sizeof(datagramm)-1)return 5;
    char antwort[512];unsigned ausführenVorgang=millisekunden();int empfangenWertAnzahl;
    do {
        empfangenWertAnzahl=datagrammDatenEmpfangen(endpunkt,antwort,sizeof(antwort),0,0,0);
        if(empfangenWertAnzahl<0&&fehlerNummer!=VersuchenErneutFehler)return 6;
    } while(empfangenWertAnzahl<0&&(unsigned)(millisekunden()-ausführenVorgang)<700);
    dateiSchließen(endpunkt);if(empfangenWertAnzahl!=sizeof(datagramm)-1)return 7;
    for(int Zahl=0;Zahl<empfangenWertAnzahl;Zahl++)if(datagramm[Zahl]!=antwort[Zahl])return 8;
    return Ausgabe("C 네트워크 überprüfen: UDP Deutsch\n");
}
