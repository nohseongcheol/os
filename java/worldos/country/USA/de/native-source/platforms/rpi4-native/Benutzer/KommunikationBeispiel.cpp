#include "NetzwerkABI.h"
static InternetNetzbuchseAdresse adresse(unsigned portWert) {
    InternetNetzbuchseAdresse Wert = {}; Wert.adresseFamilie = InternetFamilie;
    Wert.portNummer = netzwerkKurz(portWert); Wert.InternetAdresse.adresseWert = netzwerkGanzzahl(rückschleifeAdresse); return Wert;
}
extern "C" int benutzerProgrammStarten(int) {
    int sendendEndpunkt = endpunktErstellen(InternetFamilie, DatagrammNetzbuchse, 0);
    int empfängerEndpunkt = endpunktErstellen(InternetFamilie, DatagrammNetzbuchse, DatagrammProtokoll);
    if (sendendEndpunkt < 0 || empfängerEndpunkt < 0) return 1;
    InternetNetzbuchseAdresse ankunftWert = adresse(7777), abgangWert = adresse(7778), gesendetAdresse = {};
    netzbuchseAdresseLängeTyp adresseLänge = sizeof(gesendetAdresse);
    if (adresseZuordnen(empfängerEndpunkt, (NetzbuchseAdresse *)&ankunftWert, sizeof(ankunftWert))) return 2;
    if (adresseZuordnen(sendendEndpunkt, (NetzbuchseAdresse *)&ankunftWert, sizeof(ankunftWert)) != -1 || fehlerNummer != 98) return 3;
    if (adresseZuordnen(sendendEndpunkt, (NetzbuchseAdresse *)&abgangWert, sizeof(abgangWert))) return 4;
    static const char inhaltswertWert[] = "한글 UDP loopback 😀";
    char empfangenWertWert[64] = {};
    if (datagrammDatenSenden(sendendEndpunkt, inhaltswertWert, sizeof(inhaltswertWert), 0, (NetzbuchseAdresse *)&ankunftWert, sizeof(ankunftWert)) != sizeof(inhaltswertWert)) return 5;
    if (datagrammDatenEmpfangen(empfängerEndpunkt, (void *)inhaltswertWert, sizeof(inhaltswertWert), 0, 0, 0) != -1 || fehlerNummer != 14) return 6;
    if (datagrammDatenEmpfangen(empfängerEndpunkt, empfangenWertWert, sizeof(empfangenWertWert), 0, (NetzbuchseAdresse *)&gesendetAdresse, &adresseLänge) != sizeof(inhaltswertWert)) return 7;
    if (adresseLänge != sizeof(gesendetAdresse) || gerätReihenfolgeKurz(gesendetAdresse.portNummer) != 7778 || gerätReihenfolgeGanzzahl(gesendetAdresse.InternetAdresse.adresseWert) != rückschleifeAdresse) return 8;
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < sizeof(inhaltswertWert); ordnungszahlIndex++) if (empfangenWertWert[ordnungszahlIndex] != inhaltswertWert[ordnungszahlIndex]) return 9;
    if (datagrammDatenEmpfangen(empfängerEndpunkt, empfangenWertWert, sizeof(empfangenWertWert), 0, 0, 0) != -1 || fehlerNummer != 11) return 10;
    if (datagrammDatenSenden(empfängerEndpunkt, empfangenWertWert, sizeof(inhaltswertWert), 0, (NetzbuchseAdresse *)&gesendetAdresse, sizeof(gesendetAdresse)) != sizeof(inhaltswertWert)) return 11;
    if (datagrammDatenEmpfangen(sendendEndpunkt, empfangenWertWert, 4, 0, 0, 0) != 4) return 12;
    if (datagrammDatenEmpfangen(sendendEndpunkt, empfangenWertWert, 4, 0, 0, 0) != -1 || fehlerNummer != 11) return 13;
    for (int ordnungszahlIndex = 0; ordnungszahlIndex < 4; ordnungszahlIndex++) if (datagrammDatenSenden(sendendEndpunkt, inhaltswertWert, sizeof(inhaltswertWert), 0, (NetzbuchseAdresse *)&ankunftWert, sizeof(ankunftWert)) != sizeof(inhaltswertWert)) return 14;
    if (datagrammDatenSenden(sendendEndpunkt, inhaltswertWert, sizeof(inhaltswertWert), 0, (NetzbuchseAdresse *)&ankunftWert, sizeof(ankunftWert)) != -1 || fehlerNummer != 11) return 15;
    for (int ordnungszahlIndex = 0; ordnungszahlIndex < 4; ordnungszahlIndex++) if (datagrammDatenEmpfangen(empfängerEndpunkt, empfangenWertWert, sizeof(empfangenWertWert), 0, 0, 0) != sizeof(inhaltswertWert)) return 16;
    if (datagrammDatenSenden(sendendEndpunkt, 0, 0, 0, (NetzbuchseAdresse *)&ankunftWert, sizeof(ankunftWert)) != 0 ||
        datagrammDatenEmpfangen(empfängerEndpunkt, 0, 0, 0, 0, 0) != 0) return 21;
    ankunftWert.InternetAdresse.adresseWert = netzwerkGanzzahl(0x08080808);
    if (datagrammDatenSenden(sendendEndpunkt, inhaltswertWert, sizeof(inhaltswertWert), 0, (NetzbuchseAdresse *)&ankunftWert, sizeof(ankunftWert)) != -1 || fehlerNummer != 101) return 17;
    if (endpunktErstellen(InternetFamilie, DatenstromNetzwerk, DatagrammProtokoll) != -1 || fehlerNummer != 93) return 18;
    adresseLänge = sizeof(gesendetAdresse);
    if (netzbuchseAdresseLesen(empfängerEndpunkt, (NetzbuchseAdresse *)&gesendetAdresse, &adresseLänge) || gerätReihenfolgeKurz(gesendetAdresse.portNummer) != 7777) return 19;
    if (dateiSchließen(empfängerEndpunkt) || dateiSchließen(empfängerEndpunkt) != -1 || fehlerNummer != 9) return 20;
    // 보내는곳은 열어 둔다: verlassenProzessProgramm 시 프로세스별 socket 정리를 검사한다.
    static const char istFertig[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    dateiDatenSchreiben(1, istFertig, sizeof(istFertig) - 1);
    return 0;
}
