#include "../benennung/maschineBindenNamen.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Datei/Ausgabe/인수는 alleErzeugenAbbild EL0 SVC를 거친다.
#include "aufrufen.h"
#include "java-resources.h"
#include "Paket.h"
typedef uintptr_t maschineMaschinenwort;
static int kategorieWert;
static int jARAktiv, jARVerschieben;
static maschineMaschinenwort weitergeleitetArgument[8][257];
static unsigned ausstehendErsatzkode;
extern int32_t javaEintrag(void);
static intptr_t aufrufen(unsigned elementeintragAnzahl, maschineMaschinenwort ersterWert, maschineMaschinenwort zweiterWert, maschineMaschinenwort zeichenKode) {
    return benutzerAufrufen(elementeintragAnzahl, ersterWert, zweiterWert, zeichenKode, 0, 0, 0);
}
static void byteWerte(const char *datenPosition, size_t elementeintragAnzahl) { aufrufen(1, 1, (maschineMaschinenwort)datenPosition, elementeintragAnzahl); }
static void zeichen(unsigned zeichenKode) {
    unsigned char Daten[4]; unsigned elementeintragAnzahl = 0;
    if (zeichenKode < 128) Daten[elementeintragAnzahl++] = zeichenKode;
    else if (zeichenKode < 2048) { Daten[elementeintragAnzahl++] = 0xc0 | (zeichenKode >> 6); Daten[elementeintragAnzahl++] = 0x80 | (zeichenKode & 63); }
    else if (zeichenKode < 65536) { Daten[elementeintragAnzahl++] = 0xe0 | (zeichenKode >> 12); Daten[elementeintragAnzahl++] = 0x80 | ((zeichenKode >> 6) & 63); Daten[elementeintragAnzahl++] = 0x80 | (zeichenKode & 63); }
    else { Daten[elementeintragAnzahl++] = 0xf0 | (zeichenKode >> 18); Daten[elementeintragAnzahl++] = 0x80 | ((zeichenKode >> 12) & 63); Daten[elementeintragAnzahl++] = 0x80 | ((zeichenKode >> 6) & 63); Daten[elementeintragAnzahl++] = 0x80 | (zeichenKode & 63); }
    byteWerte((const char *)Daten, elementeintragAnzahl);
}
maschineMaschinenwort werkzeugZeichen(maschineMaschinenwort Wert) {
    unsigned zeichenKode = Wert;
    if (ausstehendErsatzkode) {
        unsigned hochTeil = ausstehendErsatzkode; ausstehendErsatzkode = 0;
        if (zeichenKode >= 0xdc00 && zeichenKode <= 0xdfff) { zeichen(0x10000 + ((hochTeil - 0xd800) << 10) + zeichenKode - 0xdc00); return 1; }
        zeichen(0xfffd);
    }
    if (zeichenKode >= 0xd800 && zeichenKode <= 0xdbff) ausstehendErsatzkode = zeichenKode;
    else zeichen(zeichenKode > 0x10ffff || (zeichenKode >= 0xdc00 && zeichenKode <= 0xdfff) ? 0xfffd : zeichenKode);
    return 1;
}
maschineMaschinenwort werkzeugDrucken(maschineMaschinenwort Wert) {
    const maschineMaschinenwort *zeichenketteDaten = (const maschineMaschinenwort *)Wert;
    for (maschineMaschinenwort ordnungszahlIndex = 0; ordnungszahlIndex < zeichenketteDaten[0]; ordnungszahlIndex++) werkzeugZeichen(zeichenketteDaten[ordnungszahlIndex + 1]);
    return zeichenketteDaten[0];
}
static int pfad(maschineMaschinenwort objektVerweis, char ergebnisDaten[512]) {
    const maschineMaschinenwort *ersterWert = (const maschineMaschinenwort *)objektVerweis;
    unsigned benutztKapazität = 0;
    for (maschineMaschinenwort ordnungszahlIndex = 1; ordnungszahlIndex <= ersterWert[0] && ersterWert[ordnungszahlIndex]; ordnungszahlIndex++) {
        unsigned zeichenKode = ersterWert[ordnungszahlIndex];
        // UTF-16 -> UTF-8. 기존 도구의 char[] methodeBetriebsart 경로와 호환한다.
        if (zeichenKode >= 0xd800 && zeichenKode <= 0xdbff && ordnungszahlIndex < ersterWert[0] && ersterWert[ordnungszahlIndex + 1] >= 0xdc00 && ersterWert[ordnungszahlIndex + 1] <= 0xdfff)
            { unsigned niedrigWert = ersterWert[++ordnungszahlIndex]; zeichenKode = 0x10000 + ((zeichenKode - 0xd800) << 10) + niedrigWert - 0xdc00; }
        else if (zeichenKode >= 0xd800 && zeichenKode <= 0xdfff) return -22;
        unsigned elementeintragAnzahl = zeichenKode < 128 ? 1 : zeichenKode < 2048 ? 2 : zeichenKode < 65536 ? 3 : 4;
        if (benutztKapazität + elementeintragAnzahl > 511) return -36;
        if (elementeintragAnzahl == 1) ergebnisDaten[benutztKapazität++] = zeichenKode;
        else {
            ergebnisDaten[benutztKapazität++] = (elementeintragAnzahl == 2 ? 0xc0 : elementeintragAnzahl == 3 ? 0xe0 : 0xf0) | (zeichenKode >> (6 * (elementeintragAnzahl - 1)));
            for (unsigned innerlichOrdnungszahl = elementeintragAnzahl - 1; innerlichOrdnungszahl; innerlichOrdnungszahl--) ergebnisDaten[benutztKapazität++] = 0x80 | ((zeichenKode >> (6 * (innerlichOrdnungszahl - 1))) & 63);
        }
    }
    ergebnisDaten[benutztKapazität] = 0; return benutztKapazität ? 0 : -22;
}
maschineMaschinenwort werkzeugÖffnen(maschineMaschinenwort Name, maschineMaschinenwort konfigurationBitliste) {
    char datenPosition[512]; int fehler = pfad(Name, datenPosition);
    return (uint32_t)(fehler ? fehler : aufrufen(3, (maschineMaschinenwort)datenPosition, konfigurationBitliste, 0));
}
maschineMaschinenwort werkzeugSchließen(maschineMaschinenwort dateiKennwert) { return (uint32_t)aufrufen(4, dateiKennwert, 0, 0); }
maschineMaschinenwort werkzeugLesenByte(maschineMaschinenwort dateiKennwert) {
    unsigned char zweiterWert; intptr_t elementeintragAnzahl = aufrufen(2, dateiKennwert, (maschineMaschinenwort)&zweiterWert, 1);
    return (uint32_t)(elementeintragAnzahl == 1 ? zweiterWert : elementeintragAnzahl == 0 ? 256 : elementeintragAnzahl);
}
maschineMaschinenwort werkzeugSchreibenByte(maschineMaschinenwort dateiKennwert, maschineMaschinenwort Wert) {
    unsigned char zweiterWert = Wert; return (uint32_t)aufrufen(1, dateiKennwert, (maschineMaschinenwort)&zweiterWert, 1);
}
maschineMaschinenwort werkzeugLesen(maschineMaschinenwort Name, maschineMaschinenwort zielDatenAdresse) {
    if (jARAktiv) {
        char datenPosition[512]; int fehler = pfad(Name, datenPosition); if (fehler) return (uint32_t)fehler;
        unsigned elementeintragAnzahl = 0; while (datenPosition[elementeintragAnzahl]) elementeintragAnzahl++;
        if (elementeintragAnzahl >= 6) for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl - 6; ordnungszahlIndex++) if (datenPosition[ordnungszahlIndex] == '.') datenPosition[ordnungszahlIndex] = '/';
        unsigned char byteWerte[16384]; maschineMaschinenwort *zielWertPosition = (maschineMaschinenwort *)zielDatenAdresse;
        int empfangenWertAnzahl = jARLesen(datenPosition, byteWerte, zielWertPosition[0] < sizeof(byteWerte) ? zielWertPosition[0] : sizeof(byteWerte));
        if (empfangenWertAnzahl >= 0) { for (int ordnungszahlIndex = 0; ordnungszahlIndex < empfangenWertAnzahl; ordnungszahlIndex++) zielWertPosition[ordnungszahlIndex + 1] = byteWerte[ordnungszahlIndex]; return empfangenWertAnzahl; }
        if (empfangenWertAnzahl != -2) return (uint32_t)empfangenWertAnzahl;
    }
    int dateiKennwert = jARAktiv ? -2 : (int32_t)werkzeugÖffnen(Name, 0);
    if (dateiKennwert < 0) {
        char datenPosition[512]; int fehler = pfad(Name, datenPosition); if (fehler) return (uint32_t)fehler;
        for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < sizeof(javaKlasseListe) / sizeof(javaKlasseListe[0]); ordnungszahlIndex++) {
            const char *nächsterVersatzwert = javaKlasseListe[ordnungszahlIndex].Name; unsigned innerlichOrdnungszahl = 0;
            while (datenPosition[innerlichOrdnungszahl] && datenPosition[innerlichOrdnungszahl] == nächsterVersatzwert[innerlichOrdnungszahl]) innerlichOrdnungszahl++;
            if (datenPosition[innerlichOrdnungszahl] || nächsterVersatzwert[innerlichOrdnungszahl]) continue;
            maschineMaschinenwort *zielWertPosition = (maschineMaschinenwort *)zielDatenAdresse;
            if (zielWertPosition[0] < javaKlasseListe[ordnungszahlIndex].größe) return (uint32_t)-27;
            for (innerlichOrdnungszahl = 0; innerlichOrdnungszahl < javaKlasseListe[ordnungszahlIndex].größe; innerlichOrdnungszahl++) zielWertPosition[innerlichOrdnungszahl + 1] = javaKlasseListe[ordnungszahlIndex].Daten[innerlichOrdnungszahl];
            return javaKlasseListe[ordnungszahlIndex].größe;
        }
        return (uint32_t)dateiKennwert;
    }
    maschineMaschinenwort *ersterWert = (maschineMaschinenwort *)zielDatenAdresse;
    intptr_t größe = aufrufen(9, dateiKennwert, 0, 0), abgeschlossenGesamtmenge = 0;
    if (größe < 0 || (maschineMaschinenwort)größe > ersterWert[0]) { werkzeugSchließen(dateiKennwert); return (uint32_t)(größe < 0 ? größe : -27); }
    unsigned char datenBlock[256];
    while (abgeschlossenGesamtmenge < größe) {
        intptr_t elementeintragAnzahl = aufrufen(2, dateiKennwert, (maschineMaschinenwort)datenBlock, größe - abgeschlossenGesamtmenge < 256 ? größe - abgeschlossenGesamtmenge : 256);
        if (elementeintragAnzahl <= 0) { werkzeugSchließen(dateiKennwert); return (uint32_t)(elementeintragAnzahl ? elementeintragAnzahl : -5); }
        for (intptr_t ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) ersterWert[1 + abgeschlossenGesamtmenge + ordnungszahlIndex] = datenBlock[ordnungszahlIndex];
        abgeschlossenGesamtmenge += elementeintragAnzahl;
    }
    werkzeugSchließen(dateiKennwert); return abgeschlossenGesamtmenge;
}
maschineMaschinenwort werkzeugSchreiben(maschineMaschinenwort Name, maschineMaschinenwort ursprünglichDaten, maschineMaschinenwort eintragAnzahl) {
    const maschineMaschinenwort *ersterWert = (const maschineMaschinenwort *)ursprünglichDaten;
    if (eintragAnzahl > ersterWert[0] || eintragAnzahl > 16384) return (uint32_t)-27;
    int dateiKennwert = (int32_t)werkzeugÖffnen(Name, 577); if (dateiKennwert < 0) return (uint32_t)dateiKennwert;
    unsigned char datenBlock[256]; maschineMaschinenwort abgeschlossenGesamtmenge = 0;
    while (abgeschlossenGesamtmenge < eintragAnzahl) {
        maschineMaschinenwort elementeintragAnzahl = eintragAnzahl - abgeschlossenGesamtmenge < 256 ? eintragAnzahl - abgeschlossenGesamtmenge : 256;
        for (maschineMaschinenwort ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) datenBlock[ordnungszahlIndex] = ersterWert[1 + abgeschlossenGesamtmenge + ordnungszahlIndex];
        intptr_t ergebnis = aufrufen(1, dateiKennwert, (maschineMaschinenwort)datenBlock, elementeintragAnzahl);
        if (ergebnis <= 0) { werkzeugSchließen(dateiKennwert); return (uint32_t)(ergebnis ? ergebnis : -5); }
        abgeschlossenGesamtmenge += ergebnis;
    }
    werkzeugSchließen(dateiKennwert); return eintragAnzahl;
}
maschineMaschinenwort werkzeugArgumentanzahl(void) { return aufrufen(15, UINTPTR_MAX, 0, 0) - (jARAktiv ? jARVerschieben : 0); }
maschineMaschinenwort werkzeugArgument(maschineMaschinenwort nachschlagenIndex) {
    static const maschineMaschinenwort leerwertWert[1] = {0};
    if (nachschlagenIndex >= 8) return (maschineMaschinenwort)leerwertWert;
    unsigned char eingabe[256]; intptr_t elementeintragAnzahl;
    if (jARAktiv && nachschlagenIndex == 0) { const char *datenPosition = jARHauptvorgang(); elementeintragAnzahl = 0; while (datenPosition[elementeintragAnzahl] && elementeintragAnzahl < 255) { eingabe[elementeintragAnzahl] = datenPosition[elementeintragAnzahl]; elementeintragAnzahl++; } }
    else elementeintragAnzahl = aufrufen(15, nachschlagenIndex + (jARAktiv ? jARVerschieben : 0), (maschineMaschinenwort)eingabe, sizeof(eingabe));
    if (elementeintragAnzahl < 0) return (maschineMaschinenwort)leerwertWert;
    maschineMaschinenwort *ergebnisDaten = weitergeleitetArgument[nachschlagenIndex]; unsigned eintragAnzahl = 0;
    for (intptr_t ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl;) {
        unsigned zeichenKode = eingabe[ordnungszahlIndex++], hatMehr = zeichenKode < 128 ? 0 : zeichenKode >= 0xc2 && zeichenKode < 0xe0 ? 1 : zeichenKode < 0xf0 && zeichenKode >= 0xe0 ? 2 : zeichenKode >= 0xf0 && zeichenKode <= 0xf4 ? 3 : 4;
        if (hatMehr == 4 || ordnungszahlIndex + hatMehr > elementeintragAnzahl) { ergebnisDaten[++eintragAnzahl] = 0xfffd; continue; }
        unsigned mindestwertDaten = hatMehr == 1 ? 128 : hatMehr == 2 ? 2048 : hatMehr == 3 ? 65536 : 0;
        if (hatMehr) zeichenKode &= (1u << (6 - hatMehr)) - 1;
        unsigned innerlichOrdnungszahl = 0;
        while (innerlichOrdnungszahl < hatMehr && (eingabe[ordnungszahlIndex] & 0xc0) == 0x80) { zeichenKode = (zeichenKode << 6) | (eingabe[ordnungszahlIndex++] & 63); innerlichOrdnungszahl++; }
        if (innerlichOrdnungszahl != hatMehr || zeichenKode < mindestwertDaten || zeichenKode > 0x10ffff || (zeichenKode >= 0xd800 && zeichenKode <= 0xdfff)) zeichenKode = 0xfffd;
        if (zeichenKode >= 65536) { zeichenKode -= 65536; ergebnisDaten[++eintragAnzahl] = 0xd800 | (zeichenKode >> 10); ergebnisDaten[++eintragAnzahl] = 0xdc00 | (zeichenKode & 1023); }
        else ergebnisDaten[++eintragAnzahl] = zeichenKode;
    }
    ergebnisDaten[0] = eintragAnzahl; return (maschineMaschinenwort)ergebnisDaten;
}
maschineMaschinenwort werkzeugArt(void) { return kategorieWert; }
void betriebskernNotstopp(const char *mitteilungText) {
    const char *datenPosition = mitteilungText; while (*datenPosition) datenPosition++;
    byteWerte("Java tool runtime error: ", 25); byteWerte(mitteilungText, datenPosition - mitteilungText); zeichen(10);
    aufrufen(6, 1, 0, 0); for (;;) {}
}
int benutzerProgrammStarten(int methodeBetriebsart) {
    kategorieWert = methodeBetriebsart;
    unsigned char ersterEintrag[256]; intptr_t elementeintragAnzahl = aufrufen(15, 0, (maschineMaschinenwort)ersterEintrag, sizeof(ersterEintrag));
    if (methodeBetriebsart == 2 || (methodeBetriebsart == 1 && elementeintragAnzahl == 4 && ersterEintrag[0] == '-' && ersterEintrag[1] == 'j' && ersterEintrag[2] == 'a' && ersterEintrag[3] == 'r')) {
        jARVerschieben = methodeBetriebsart == 2 ? 0 : 1;
        char dateiEintragName[256]; intptr_t längeDaten = aufrufen(15, jARVerschieben, (maschineMaschinenwort)dateiEintragName, sizeof(dateiEintragName));
        if (längeDaten <= 0 || jARÖffnen(dateiEintragName) < 0) {
            static const char fehler[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            byteWerte(fehler, sizeof(fehler) - 1); return 1;
        }
        jARAktiv = 1;
    }
    int ergebnis = javaEintrag();
    if (ausstehendErsatzkode) zeichen(0xfffd);
    return ergebnis;
}

// UDP는 eigen 커널의 SVC를 통과하며 aktuellElementeintrag 127.0.0.1만 제공한다.
struct javaAdresse { uint16_t familie, portNummer; uint32_t adresse; unsigned char nullwertWert[8]; };
static struct javaAdresse uDPAdresse(unsigned portNummer) {
    struct javaAdresse ersterWert = {2, (uint16_t)((portNummer << 8) | (portNummer >> 8)), 0x0100007f, {0}}; return ersterWert;
}
maschineMaschinenwort werkzeugUDPÖffnen(maschineMaschinenwort portNummer) {
    intptr_t dateiKennwert = aufrufen(32, 2, 2, 17); if (dateiKennwert < 0) return (uint32_t)dateiKennwert;
    struct javaAdresse ersterWert = uDPAdresse(portNummer);
    ersterWert.adresse = 0;
    intptr_t statuswertWert = aufrufen(33, dateiKennwert, (maschineMaschinenwort)&ersterWert, sizeof(ersterWert));
    if (statuswertWert < 0) { werkzeugSchließen(dateiKennwert); return (uint32_t)statuswertWert; }
    return dateiKennwert;
}
maschineMaschinenwort werkzeugUDPSenden(maschineMaschinenwort dateiKennwert, maschineMaschinenwort portNummer, maschineMaschinenwort datenfeldWert, maschineMaschinenwort Länge) {
    const maschineMaschinenwort *ursprünglichAdresse = (const maschineMaschinenwort *)datenfeldWert; unsigned char Daten[512];
    if (Länge > 512 || Länge > ursprünglichAdresse[0]) return (uint32_t)-90;
    for (maschineMaschinenwort ordnungszahlIndex = 0; ordnungszahlIndex < Länge; ordnungszahlIndex++) Daten[ordnungszahlIndex] = ursprünglichAdresse[ordnungszahlIndex + 1];
    struct javaAdresse ersterWert = uDPAdresse(portNummer);
    return (uint32_t)benutzerAufrufen(34, dateiKennwert, (maschineMaschinenwort)Daten, Länge, 0, (maschineMaschinenwort)&ersterWert, sizeof(ersterWert));
}
static uint32_t rückwärtsByteReihenfolge(uint32_t elementeintragAnzahl) { return (elementeintragAnzahl>>24)|((elementeintragAnzahl>>8)&0xff00)|((elementeintragAnzahl<<8)&0xff0000)|(elementeintragAnzahl<<24); }
maschineMaschinenwort werkzeugUDPSendenAdresse(maschineMaschinenwort dateiKennwert, maschineMaschinenwort adresse, maschineMaschinenwort portNummer, maschineMaschinenwort datenfeldWert, maschineMaschinenwort Länge) {
    const maschineMaschinenwort *ursprünglichAdresse = (const maschineMaschinenwort *)datenfeldWert; unsigned char Daten[512];
    if (Länge > 512 || Länge > ursprünglichAdresse[0]) return (uint32_t)-90;
    for (maschineMaschinenwort ordnungszahlIndex = 0; ordnungszahlIndex < Länge; ordnungszahlIndex++) Daten[ordnungszahlIndex] = ursprünglichAdresse[ordnungszahlIndex + 1];
    struct javaAdresse ersterWert = uDPAdresse(portNummer); ersterWert.adresse = rückwärtsByteReihenfolge(adresse);
    return (uint32_t)benutzerAufrufen(34, dateiKennwert, (maschineMaschinenwort)Daten, Länge, 0, (maschineMaschinenwort)&ersterWert, sizeof(ersterWert));
}
maschineMaschinenwort werkzeugVerbinden(maschineMaschinenwort dateiKennwert, maschineMaschinenwort adresse, maschineMaschinenwort portNummer) {
    struct javaAdresse ersterWert = uDPAdresse(portNummer); ersterWert.adresse = rückwärtsByteReihenfolge(adresse);
    uint32_t ausführenVorgang = aufrufen(7, 0, 0, 0);
    for (;;) {
        intptr_t ergebnis = aufrufen(37, dateiKennwert, (maschineMaschinenwort)&ersterWert, sizeof(ersterWert));
        if (ergebnis != -115) return (uint32_t)ergebnis;
        if ((uint32_t)(aufrufen(7, 0, 0, 0) - ausführenVorgang) >= 1000) return (uint32_t)-110;
    }
}
maschineMaschinenwort werkzeugUDPEmpfangsvorgang(maschineMaschinenwort dateiKennwert, maschineMaschinenwort datenfeldWert, maschineMaschinenwort pufferKapazität) {
    maschineMaschinenwort *zielAdresse = (maschineMaschinenwort *)datenfeldWert; unsigned char Daten[512];
    if (pufferKapazität > 512 || zielAdresse[0] < 514) return (uint32_t)-90;
    struct javaAdresse ersterWert; unsigned längeDaten = sizeof(ersterWert);
    intptr_t elementeintragAnzahl = benutzerAufrufen(35, dateiKennwert, (maschineMaschinenwort)Daten, pufferKapazität, 0, (maschineMaschinenwort)&ersterWert, (maschineMaschinenwort)&längeDaten);
    if (elementeintragAnzahl >= 0) { for (intptr_t ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) zielAdresse[ordnungszahlIndex + 1] = Daten[ordnungszahlIndex]; zielAdresse[513] = (ersterWert.portNummer << 8 | ersterWert.portNummer >> 8) & 65535; zielAdresse[514] = rückwärtsByteReihenfolge(ersterWert.adresse); }
    return (uint32_t)elementeintragAnzahl;
}
maschineMaschinenwort werkzeugUDPPort(maschineMaschinenwort dateiKennwert) {
    struct javaAdresse ersterWert; unsigned längeDaten = sizeof(ersterWert);
    intptr_t zurückgegebenWert = aufrufen(36, dateiKennwert, (maschineMaschinenwort)&ersterWert, (maschineMaschinenwort)&längeDaten);
    return (uint32_t)(zurückgegebenWert < 0 ? zurückgegebenWert : (ersterWert.portNummer << 8 | ersterWert.portNummer >> 8) & 65535);
}
maschineMaschinenwort werkzeugVergangeneMillisekunden(void) { return (uint32_t)aufrufen(7, 0, 0, 0); }
maschineMaschinenwort werkzeugBildschirmBreite(void) { return (uint32_t)bildschirmBreiteLesen(); }
maschineMaschinenwort werkzeugBildschirmHöhe(void) { return (uint32_t)bildschirmHöheLesen(); }
maschineMaschinenwort werkzeugGrafikWarten(void) { return (uint32_t)fürBildschirmTasteWarten(); }
maschineMaschinenwort werkzeugRechteck(maschineMaschinenwort waagerechteKoordinateKoordinate, maschineMaschinenwort senkrechteKoordinateKoordinate, maschineMaschinenwort angefordertBreiteWert, maschineMaschinenwort angefordertHöheWert, maschineMaschinenwort bildpunktFarbe) {
    return (uint32_t)benutzerAufrufen(13, waagerechteKoordinateKoordinate, senkrechteKoordinateKoordinate, bildpunktFarbe, angefordertBreiteWert, angefordertHöheWert, 0);
}

maschineMaschinenwort werkzeugDatenstrom(maschineMaschinenwort aktion,maschineMaschinenwort dateiKennwert,maschineMaschinenwort Wert){
    if(aktion==0)return (uint32_t)aufrufen(32,2,1,6);
    struct javaAdresse ersterWert=uDPAdresse(Wert);
    if(aktion==1){ersterWert.adresse=0;intptr_t zurückgegebenWert=aufrufen(33,dateiKennwert,(maschineMaschinenwort)&ersterWert,sizeof(ersterWert));return (uint32_t)(zurückgegebenWert<0?zurückgegebenWert:aufrufen(38,dateiKennwert,4,0));}
    if(aktion==2)return (uint32_t)aufrufen(37,dateiKennwert,(maschineMaschinenwort)&ersterWert,sizeof(ersterWert));
    if(aktion==3)return (uint32_t)aufrufen(39,dateiKennwert,0,0);
    if(aktion==4)return werkzeugUDPPort(dateiKennwert);
    if(aktion==5)return (uint32_t)aufrufen(40,dateiKennwert,0,0);
    return (uint32_t)-22;
}
maschineMaschinenwort werkzeugGUI(maschineMaschinenwort aktion,maschineMaschinenwort bezeichnerWert,maschineMaschinenwort ersterWert,maschineMaschinenwort zweiterWert,maschineMaschinenwort zeichenKode,maschineMaschinenwort zielDaten){return (uint32_t)benutzerAufrufen(20,aktion,bezeichnerWert,ersterWert,zweiterWert,zeichenKode,zielDaten);}
maschineMaschinenwort werkzeugGUIText(maschineMaschinenwort bezeichnerWert,maschineMaschinenwort datenfeldWert,maschineMaschinenwort elementeintragAnzahl){
    const maschineMaschinenwort *ursprünglichAdresse=(const maschineMaschinenwort *)datenfeldWert;uint32_t Daten[127];unsigned eintragAnzahl=0;
    if(elementeintragAnzahl>ursprünglichAdresse[0])return (uint32_t)-22;
    for(maschineMaschinenwort ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++){unsigned zeichenKodierung=ursprünglichAdresse[ordnungszahlIndex+1];if(zeichenKodierung>=0xd800&&zeichenKodierung<=0xdbff&&ordnungszahlIndex+1<elementeintragAnzahl){unsigned niedrigWert=ursprünglichAdresse[++ordnungszahlIndex+1];if(niedrigWert<0xdc00||niedrigWert>0xdfff)return (uint32_t)-22;zeichenKodierung=0x10000+((zeichenKodierung-0xd800)<<10)+niedrigWert-0xdc00;}if(eintragAnzahl==127)return (uint32_t)-22;Daten[eintragAnzahl++]=zeichenKodierung;}
    return (uint32_t)benutzerAufrufen(21,bezeichnerWert,(maschineMaschinenwort)Daten,eintragAnzahl,0,0,0);
}
