#include "../benennung/maschineBindenNamen.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Netzwerkstapel.h"
#include "string.h"
#include "DateiABI.h"
extern uintptr_t platineVergangeneMillisekunden(void);
extern int32_t javaDateisystemEintragLänge(int32_t), javaDateisystemEintragByte(int32_t,int32_t), javaDateisystemEintragGröße(int32_t);
extern int32_t javaDateisystemEintragAnzahl(void);
static int portEmpfangen = -1, steuerung = -1, handbuchVerbindung = -1, Daten = -1;
static unsigned istProtokolliertEingehend, benutzerInOrdnung, zeileGröße, zeileFehlerhaft, aufhörenProgramm, ausführendAufgabe, benutztKapazität, gesendetAnzahl, hatFehlgeschlagen;
static unsigned antwortGröße, antwortGesendet, nächsterPortNummer;
static uint32_t aktivität;
static char zeile[256], antworten[2048], dateiEintragName[64], übertragungName[64];
static unsigned char übertragungStatuswert[16384];
static int gleich(const char *ersterWert, const char *zweiterWert) { while (*ersterWert && *ersterWert == *zweiterWert) { ersterWert++; zweiterWert++; } return *ersterWert == *zweiterWert; }
static void antwort(const char *zeichenketteDaten) {
    size_t elementeintragAnzahl = strlen(zeichenketteDaten);
    if (antwortGesendet) { memmove(antworten, antworten + antwortGesendet, antwortGröße - antwortGesendet); antwortGröße -= antwortGesendet; antwortGesendet = 0; }
    if (elementeintragAnzahl > sizeof(antworten) - antwortGröße) { aufhörenProgramm = 1; return; }
    memcpy(antworten + antwortGröße, zeichenketteDaten, elementeintragAnzahl); antwortGröße += elementeintragAnzahl;
}
static void numerischWert(unsigned Wert, char *ergebnisDaten, unsigned *elementeintragAnzahl) {
    char zifferAnzahl[10]; unsigned eintragAnzahl = 0;
    do { zifferAnzahl[eintragAnzahl++] = '0' + Wert % 10; Wert /= 10; } while (Wert);
    while (eintragAnzahl) ergebnisDaten[(*elementeintragAnzahl)++] = zifferAnzahl[--eintragAnzahl];
}
static void übertragungStoppen(void) {
    if (Daten >= 0) netzwerkSchließen(Daten); if (handbuchVerbindung >= 0) netzwerkSchließen(handbuchVerbindung);
    Daten = handbuchVerbindung = -1; ausführendAufgabe = benutztKapazität = gesendetAnzahl = hatFehlgeschlagen = 0;
}
static void trennen(void) {
    übertragungStoppen(); if (steuerung >= 0) netzwerkSchließen(steuerung); steuerung = -1;
    istProtokolliertEingehend = benutzerInOrdnung = zeileGröße = zeileFehlerhaft = antwortGröße = antwortGesendet = aufhörenProgramm = 0;
}
int dateiÜbertragungSteuerung(int aktion) {
    if (aktion == 2) return portEmpfangen >= 0;
    if (aktion == 0) { trennen(); if (portEmpfangen >= 0) netzwerkSchließen(portEmpfangen); portEmpfangen = -1; return 0; }
    if (aktion != 1) return -22; if (portEmpfangen >= 0) return 0;
    portEmpfangen = netzbuchseEndpunktErstellen(1); if (portEmpfangen < 0) return portEmpfangen;
    int zurückgegebenWert = netzZuordnen(portEmpfangen, netzwerkZustandLesen(0,0), 21); if (!zurückgegebenWert) zurückgegebenWert = netzLauschen(portEmpfangen);
    if (zurückgegebenWert < 0) { netzwerkSchließen(portEmpfangen); portEmpfangen = -1; } return zurückgegebenWert;
}
static int pfad(const char *Name) {
    unsigned elementeintragAnzahl = 0; if (*Name == '/') Name++;
    if (!*Name || gleich(Name, ".") || gleich(Name, "..")) return 0;
    dateiEintragName[elementeintragAnzahl++] = '/';
    while (*Name) {
        unsigned char zeichenKode = *Name++;
        if (elementeintragAnzahl >= 63 || zeichenKode < 32 || zeichenKode == 127 || zeichenKode == '/' || zeichenKode == '\\') return 0;
        dateiEintragName[elementeintragAnzahl++] = zeichenKode;
    }
    dateiEintragName[elementeintragAnzahl] = 0; return 1;
}
static void listeSenden(int einzelheit) {
    benutztKapazität = gesendetAnzahl = 0;
    for (int ordnungszahlIndex = 0; ordnungszahlIndex < javaDateisystemEintragAnzahl(); ordnungszahlIndex++) {
        int elementeintragAnzahl = javaDateisystemEintragLänge(ordnungszahlIndex); if (elementeintragAnzahl <= 0) continue;
        const char *voranstehendTeil = einzelheit == 2 ? "type=file;size=" : einzelheit == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned eintragAnzahl = strlen(voranstehendTeil); memcpy(übertragungStatuswert + benutztKapazität, voranstehendTeil, eintragAnzahl); benutztKapazität += eintragAnzahl;
        if (einzelheit) numerischWert(javaDateisystemEintragGröße(ordnungszahlIndex), (char *)übertragungStatuswert, &benutztKapazität);
        const char *nachsilbeWert = einzelheit == 2 ? "; " : einzelheit == 1 ? " Jan 01 00:00 " : "";
        eintragAnzahl = strlen(nachsilbeWert); memcpy(übertragungStatuswert + benutztKapazität, nachsilbeWert, eintragAnzahl); benutztKapazität += eintragAnzahl;
        for (int innerlichOrdnungszahl = 0; innerlichOrdnungszahl < elementeintragAnzahl; innerlichOrdnungszahl++) übertragungStatuswert[benutztKapazität++] = javaDateisystemEintragByte(ordnungszahlIndex,innerlichOrdnungszahl);
        übertragungStatuswert[benutztKapazität++] = '\r'; übertragungStatuswert[benutztKapazität++] = '\n';
    }
}
static void handbuchVerbindungVorbereiten(int erweitert) {
    if (ausführendAufgabe) { antwort("450 Transfer in progress\r\n"); return; }
    übertragungStoppen(); handbuchVerbindung = netzbuchseEndpunktErstellen(1);
    if (handbuchVerbindung >= 0) wiederverwendenNetzbuchseAdresse(handbuchVerbindung);
    unsigned portNummer = 50000 + nächsterPortNummer++ % 8;
    if (handbuchVerbindung < 0 || netzZuordnen(handbuchVerbindung, netzwerkZustandLesen(0,0), portNummer) || netzLauschen(handbuchVerbindung)) {
        übertragungStoppen(); antwort("425 Cannot open passive listener\r\n"); return;
    }
    char rückmeldung[96]; const char *voranstehendTeil = erweitert ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned elementeintragAnzahl = strlen(voranstehendTeil); memcpy(rückmeldung, voranstehendTeil, elementeintragAnzahl);
    if (erweitert) { numerischWert(portNummer, rückmeldung, &elementeintragAnzahl); rückmeldung[elementeintragAnzahl++] = '|'; }
    else {
        uint32_t adresse=netzwerkZustandLesen(0,0);
        for (int positionIndex=24;positionIndex>=0;positionIndex-=8) { numerischWert((adresse>>positionIndex)&255,rückmeldung,&elementeintragAnzahl);rückmeldung[elementeintragAnzahl++]=','; }
        numerischWert(portNummer / 256, rückmeldung, &elementeintragAnzahl); rückmeldung[elementeintragAnzahl++] = ','; numerischWert(portNummer % 256, rückmeldung, &elementeintragAnzahl);
    }
    rückmeldung[elementeintragAnzahl++] = ')'; rückmeldung[elementeintragAnzahl++] = '\r'; rückmeldung[elementeintragAnzahl++] = '\n'; rückmeldung[elementeintragAnzahl] = 0; antwort(rückmeldung);
}
static void befehl(void) {
    zeile[zeileGröße] = 0;
    char *zusätzlichArgumente = zeile; while (*zusätzlichArgumente && *zusätzlichArgumente != ' ') { if (*zusätzlichArgumente >= 'a' && *zusätzlichArgumente <= 'z') *zusätzlichArgumente -= 32; zusätzlichArgumente++; }
    if (*zusätzlichArgumente) *zusätzlichArgumente++ = 0; while (*zusätzlichArgumente == ' ') zusätzlichArgumente++;
    if (gleich(zeile, "QUIT")) { übertragungStoppen(); antwort("221 Goodbye\r\n"); aufhörenProgramm = 1; return; }
    if (gleich(zeile, "NOOP")) { antwort("200 OK\r\n"); return; }
    if (gleich(zeile, "SYST")) { antwort("215 UNIX Type: L8\r\n"); return; }
    if (gleich(zeile, "FEAT")) { antwort("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (gleich(zeile, "USER")) { istProtokolliertEingehend = 0; benutzerInOrdnung = gleich(zusätzlichArgumente, "anonymous") || gleich(zusätzlichArgumente, "jkoros"); antwort(benutzerInOrdnung ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (gleich(zeile, "PASS")) { istProtokolliertEingehend = benutzerInOrdnung; antwort(istProtokolliertEingehend ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!istProtokolliertEingehend) { antwort("530 Login first\r\n"); return; }
    if (gleich(zeile, "PWD")) antwort("257 \"/\"\r\n");
    else if (gleich(zeile, "CWD")) antwort(gleich(zusätzlichArgumente, "/") || gleich(zusätzlichArgumente, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (gleich(zeile, "TYPE")) antwort(gleich(zusätzlichArgumente, "I") || gleich(zusätzlichArgumente, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (gleich(zeile, "OPTS")) antwort(gleich(zusätzlichArgumente, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (gleich(zeile, "PASV")) handbuchVerbindungVorbereiten(0);
    else if (gleich(zeile, "EPSV")) { if (*zusätzlichArgumente && !gleich(zusätzlichArgumente, "1")) antwort("522 IPv4 only\r\n"); else handbuchVerbindungVorbereiten(1); }
    else if (gleich(zeile, "ABOR")) { übertragungStoppen(); antwort("226 Transfer aborted\r\n"); }
    else if (gleich(zeile, "DELE")) { antwort(pfad(zusätzlichArgumente) && pk_unlink(dateiEintragName) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (gleich(zeile, "LIST") || gleich(zeile, "NLST") || gleich(zeile, "MLSD")) {
        if (ausführendAufgabe) { antwort("450 Transfer in progress\r\n"); return; }
        if (handbuchVerbindung < 0 && Daten < 0) { antwort("425 Use PASV or EPSV\r\n"); return; }
        if (*zusätzlichArgumente && !gleich(zusätzlichArgumente,"/") && !gleich(zusätzlichArgumente,".") && !gleich(zusätzlichArgumente,"-a") && !gleich(zusätzlichArgumente,"-l") && !gleich(zusätzlichArgumente,"-la")) { antwort("550 Root listing only\r\n"); return; }
        listeSenden(gleich(zeile,"MLSD") ? 2 : gleich(zeile,"LIST") ? 1 : 0); ausführendAufgabe = 2;
        antwort("150 Opening directory listing\r\n");
    }
    else if (gleich(zeile, "SIZE")) {
        if (!pfad(zusätzlichArgumente)) { antwort("550 Invalid filename\r\n"); return; }
        int dateiKennwert = pk_open(dateiEintragName, ausschließlichWertLesen, 0); if (dateiKennwert < 0) { antwort("550 File unavailable\r\n"); return; }
        int größe = pk_size(dateiKennwert); pk_close(dateiKennwert); char rückmeldung[32] = "213 "; unsigned elementeintragAnzahl = 4;
        numerischWert(größe, rückmeldung, &elementeintragAnzahl); rückmeldung[elementeintragAnzahl++] = '\r'; rückmeldung[elementeintragAnzahl++] = '\n'; rückmeldung[elementeintragAnzahl] = 0; antwort(rückmeldung);
    } else if (gleich(zeile, "STOR") || gleich(zeile, "RETR")) {
        if (ausführendAufgabe) { antwort("450 Transfer in progress\r\n"); return; }
        if (handbuchVerbindung < 0 && Daten < 0) { antwort("425 Use PASV or EPSV\r\n"); return; }
        if (!pfad(zusätzlichArgumente)) { antwort("550 Invalid filename\r\n"); return; }
        ausführendAufgabe = gleich(zeile, "STOR") ? 1 : 2; benutztKapazität = gesendetAnzahl = hatFehlgeschlagen = 0;
        memcpy(übertragungName, dateiEintragName, strlen(dateiEintragName) + 1);
        if (ausführendAufgabe == 2) {
            int dateiKennwert = pk_open(dateiEintragName, ausschließlichWertLesen, 0);
            if (dateiKennwert < 0) { ausführendAufgabe = 0; antwort("550 File unavailable\r\n"); return; }
            int elementeintragAnzahl = pk_read(dateiKennwert, übertragungStatuswert, sizeof(übertragungStatuswert)); pk_close(dateiKennwert);
            if (elementeintragAnzahl < 0) { ausführendAufgabe = 0; antwort("451 Read failed\r\n"); return; } benutztKapazität = elementeintragAnzahl;
        }
        antwort("150 Opening binary data connection\r\n");
    } else antwort("502 Command not implemented\r\n");
}
void dateiÜbertragungUntersuchen(void) {
    if (portEmpfangen < 0) return;
    int eintreffendVerbindung = netzAnnehmen(portEmpfangen);
    if (eintreffendVerbindung >= 0) {
        if (steuerung >= 0) { netzSchreiben(eintreffendVerbindung, "421 One session at a time\r\n", 27); netzwerkSchließen(eintreffendVerbindung); }
        else { steuerung = eintreffendVerbindung; aktivität = platineVergangeneMillisekunden(); antwort("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (steuerung < 0) return;
    if ((uint32_t)(platineVergangeneMillisekunden() - aktivität) > 60000) { trennen(); return; }
    if (!aufhörenProgramm) for (unsigned vorrat = 0; vorrat < 256; vorrat++) {
        unsigned char zeichenKode; int zurückgegebenWert = netzLesen(steuerung, &zeichenKode, 1);
        if (zurückgegebenWert == -11) break; if (zurückgegebenWert <= 0) { trennen(); return; } aktivität = platineVergangeneMillisekunden();
        if (zeichenKode == '\n') { if (zeileFehlerhaft) antwort("500 Command too long or invalid\r\n"); else befehl(); zeileGröße = zeileFehlerhaft = 0; if (aufhörenProgramm) break; }
        else if (zeichenKode != '\r') { if (!zeichenKode || zeileGröße >= sizeof(zeile) - 1) zeileFehlerhaft = 1; else zeile[zeileGröße++] = zeichenKode; }
    }
    if (handbuchVerbindung >= 0 && Daten < 0) {
        int zurückgegebenWert = netzAnnehmen(handbuchVerbindung);
        if (zurückgegebenWert >= 0) {
            if (netzGegenstelleAdresse(zurückgegebenWert) != netzGegenstelleAdresse(steuerung)) netzwerkSchließen(zurückgegebenWert);
            else { Daten = zurückgegebenWert; netzwerkSchließen(handbuchVerbindung); handbuchVerbindung = -1; aktivität = platineVergangeneMillisekunden(); }
        }
    }
    if (ausführendAufgabe == 1 && Daten >= 0) for (unsigned vorrat = 0; vorrat < 8; vorrat++) {
        unsigned char datenBlock[512]; int elementeintragAnzahl = netzLesen(Daten, datenBlock, sizeof(datenBlock));
        if (elementeintragAnzahl == -11) break;
        if (elementeintragAnzahl < 0) { übertragungStoppen(); antwort("426 Data connection failed\r\n"); break; }
        aktivität = platineVergangeneMillisekunden();
        if (elementeintragAnzahl == 0) {
            int ergebnis = -1;
            if (!hatFehlgeschlagen) {
                int dateiKennwert = pk_open(übertragungName, ausschließlichWertSchreiben | ErstellenFallsFehlend | KürzenInhalt, 0600);
                if (dateiKennwert >= 0) { ergebnis = pk_write(dateiKennwert, übertragungStatuswert, benutztKapazität); pk_close(dateiKennwert); }
            }
            int istErfolgreich = !hatFehlgeschlagen && ergebnis == (int)benutztKapazität; übertragungStoppen(); antwort(istErfolgreich ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)elementeintragAnzahl > sizeof(übertragungStatuswert) - benutztKapazität) hatFehlgeschlagen = 1;
        if (!hatFehlgeschlagen) { memcpy(übertragungStatuswert + benutztKapazität, datenBlock, elementeintragAnzahl); benutztKapazität += elementeintragAnzahl; }
    }
    if (ausführendAufgabe == 2 && Daten >= 0) {
        int elementeintragAnzahl = netzSchreiben(Daten, übertragungStatuswert + gesendetAnzahl, benutztKapazität - gesendetAnzahl);
        if (elementeintragAnzahl >= 0) { gesendetAnzahl += elementeintragAnzahl; aktivität = platineVergangeneMillisekunden(); if (gesendetAnzahl == benutztKapazität) { übertragungStoppen(); antwort("226 Transfer complete\r\n"); } }
        else if (elementeintragAnzahl != -11) { übertragungStoppen(); antwort("426 Data connection failed\r\n"); }
    }
    if (antwortGesendet < antwortGröße) {
        int elementeintragAnzahl = netzSchreiben(steuerung, antworten + antwortGesendet, antwortGröße - antwortGesendet);
        if (elementeintragAnzahl > 0) antwortGesendet += elementeintragAnzahl; else if (elementeintragAnzahl != -11) { trennen(); return; }
    }
    if (antwortGesendet == antwortGröße) { antwortGröße = antwortGesendet = 0; if (aufhörenProgramm) trennen(); }
}
