#include "../benennung/maschineBindenNamen.h"
#include "DateiABI.h"
// 표준 C++ bibliothek 없는 freestanding C++11 Programm. 커널에 statischWert 링크한다.
extern "C" uintptr_t cppProgrammePrüfung(void) {
    const char inhaltswertWert[] = "C++ → Java betriebskernWert · 한글 😀";
    unsigned char wertLesen[sizeof(inhaltswertWert)] = {};
    int Datei = dateiÖffnen("Prüfungen.txt", LesenSchreiben | ErstellenFallsFehlend | KürzenInhalt, 0600);
    if (Datei < 0) return 1;
    if (dateiDatenSchreiben(Datei, inhaltswertWert, sizeof(inhaltswertWert)) != sizeof(inhaltswertWert)) return 2;
    if (dateiPositionieren(Datei, 0, VonAnfang) != 0) return 3;
    if (dateiDatenLesen(Datei, wertLesen, sizeof(wertLesen)) != sizeof(wertLesen)) return 4;
    for (size_t ordnungszahlIndex = 0; ordnungszahlIndex < sizeof(inhaltswertWert); ordnungszahlIndex++) if (wertLesen[ordnungszahlIndex] != (unsigned char)inhaltswertWert[ordnungszahlIndex]) return 5;
    if (dateiDatenLesen(Datei, wertLesen, 1) != 0) return 6;
    if (bestätigenDateiSpeichergerät(Datei) != -1 || fehlerNummer != 38) return 7;
    if (dateiSchließen(Datei) || dateiSchließen(Datei) != -1 || fehlerNummer != 9) return 8;
    Datei = dateiÖffnen("Prüfungen.txt", ausschließlichWertLesen);
    if (Datei < 0 || dateiDatenSchreiben(Datei, inhaltswertWert, 1) != -1 || fehlerNummer != 9) return 9;
    if (dateiSchließen(Datei)) return 10;
    Datei = dateiÖffnen("Prüfungen.txt", LesenSchreiben | anStelleEndeAnhängen);
    if (Datei < 0 || dateiPositionieren(Datei, 0, VonAnfang) != 0 || dateiDatenSchreiben(Datei, "!", 1) != 1 || dateiGröße(Datei) != sizeof(inhaltswertWert) + 1) return 11;
    if (dateiLängeSetzen(Datei, 2) || dateiPositionieren(Datei, 4, VonAnfang) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (dateiDatenSchreiben(Datei, "x", 1) != 1 || dateiGröße(Datei) != 3 || dateiSchließen(Datei)) return 13;
    Datei = dateiÖffnen("구멍.bin", LesenSchreiben | ErstellenFallsFehlend | KürzenInhalt, 0600);
    if (Datei < 0 || dateiPositionieren(Datei, 3, VonAnfang) != 3 || dateiDatenSchreiben(Datei, "z", 1) != 1) return 14;
    if (dateiPositionieren(Datei, 0, VonAnfang) != 0 || dateiDatenLesen(Datei, wertLesen, 4) != 4 || wertLesen[0] || wertLesen[1] || wertLesen[2] || wertLesen[3] != 'z') return 15;
    if (dateiEintragNameEntfernen("구멍.bin") || dateiGröße(Datei) != 4 || dateiSchließen(Datei)) return 16;
    if (dateiÖffnen("구멍.bin", ausschließlichWertLesen) != -1 || fehlerNummer != 2) return 17;
    if (dateiÖffnen("Prüfungen.txt", LesenSchreiben | neuDateiErstellen, 0600) != -1 || fehlerNummer != 17) return 18;
    if (dateiÖffnen("../unzulässigWert", ausschließlichWertLesen) != -1) return 19;
    return 0;
}
