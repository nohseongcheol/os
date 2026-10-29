#include "NetzwerkABI.h"

int benutzerProgrammStarten(int argumente) {
    (void)argumente;
    struct InternetNetzbuchseAdresse adresse = {0};
    adresse.adresseFamilie = InternetFamilie;
    adresse.portNummer = netzwerkKurz(9260);
    adresse.InternetAdresse.adresseWert = netzwerkGanzzahl(rückschleifeAdresse);
    int dienstanbieterWert = endpunktErstellen(InternetFamilie, DatenstromNetzwerk, datenstromBeförderungProtokoll);
    if (dienstanbieterWert < 0 || adresseZuordnen(dienstanbieterWert, (struct NetzbuchseAdresse *)&adresse, sizeof(adresse)) < 0 ||
        fürNetzwerkVerbindungWarten(dienstanbieterWert, 4) < 0) return 1;
    if (netzwerkVerbindungAnnehmen(dienstanbieterWert, 0, 0) != -1 || fehlerNummer != 11) return 2;
    int gastWert = endpunktErstellen(InternetFamilie, DatenstromNetzwerk, datenstromBeförderungProtokoll);
    if (gastWert < 0 || netzwerkVerbinden(gastWert, (struct NetzbuchseAdresse *)&adresse, sizeof(adresse)) < 0) return 3;
    int verbinden = netzwerkVerbindungAnnehmen(dienstanbieterWert, 0, 0);
    if (verbinden < 0) return 4;
    unsigned char elementeintragNachSenden[1500], empfangenWertElementeintrag[1500];
    for (int Zahl = 0; Zahl < 1500; Zahl++) elementeintragNachSenden[Zahl] = (unsigned char)Zahl;
    int gesendetAnzahl = 0;
    while (gesendetAnzahl < 1024) {
        int Länge = dateiDatenSchreiben(gastWert, elementeintragNachSenden + gesendetAnzahl, sizeof(elementeintragNachSenden) - gesendetAnzahl);
        if (Länge <= 0) return 5;
        gesendetAnzahl += Länge;
    }
    if (dateiDatenSchreiben(gastWert, elementeintragNachSenden, 1) != -1 || fehlerNummer != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 alleErzeugenAbbild 읽은 rückseiteWert EOF가 된다. */
    dateiSchließen(gastWert);
    int empfangenWertAnzahl = 0;
    while (empfangenWertAnzahl < gesendetAnzahl) {
        int Länge = dateiDatenLesen(verbinden, empfangenWertElementeintrag + empfangenWertAnzahl, sizeof(empfangenWertElementeintrag) - empfangenWertAnzahl);
        if (Länge <= 0) return 7;
        empfangenWertAnzahl += Länge;
    }
    for (int Zahl = 0; Zahl < empfangenWertAnzahl; Zahl++) if (empfangenWertElementeintrag[Zahl] != elementeintragNachSenden[Zahl]) return 8;
    if (dateiDatenLesen(verbinden, empfangenWertElementeintrag, 1) != 0) return 9;
    if (dateiDatenSchreiben(verbinden, elementeintragNachSenden, 1) != -1 || fehlerNummer != 32) return 10;
    dateiSchließen(verbinden); dateiSchließen(dienstanbieterWert);
    const char ergebnis[] = "C posix-kor 연결형 Kommunikation PASS\n";
    dateiDatenSchreiben(1, ergebnis, sizeof(ergebnis) - 1);
    return 0;
}
