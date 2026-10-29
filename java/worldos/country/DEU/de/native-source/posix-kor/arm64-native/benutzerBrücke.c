// 동일 Deutsch 헤더를 사용하는 별도 EL0 bibliothek. betriebskernWert 직접 호출판과 혼합 unzulässigWert.
#include "DateiABI.h"
#include "aufrufen.h"
#include "NetzwerkABI.h"
static int fehlerKode;
int *pk_errno_location(void) { return &fehlerKode; }
static intptr_t geprüft(intptr_t ergebnis) { if (ergebnis < 0) { fehlerKode = -ergebnis; return -1; } return ergebnis; }
int pk_open(const char *path, int flags, ...) { return geprüft(benutzerAufrufen(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
einAusgabeErgebnisTyp pk_read(int fd, void *p, size_t n) { return geprüft(benutzerAufrufen(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
einAusgabeErgebnisTyp pk_write(int fd, const void *p, size_t n) { return geprüft(benutzerAufrufen(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return geprüft(benutzerAufrufen(4, fd, 0, 0, 0, 0, 0)); }
dateiVersatzwertTyp pk_lseek(int fd, dateiVersatzwertTyp offset, int origin) { return geprüft(benutzerAufrufen(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return geprüft(benutzerAufrufen(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, dateiVersatzwertTyp size) { return geprüft(benutzerAufrufen(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return geprüft(benutzerAufrufen(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return geprüft(benutzerAufrufen(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return geprüft(benutzerAufrufen(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return geprüft(benutzerAufrufen(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return geprüft(benutzerAufrufen(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return geprüft(benutzerAufrufen(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return geprüft(benutzerAufrufen(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return geprüft(benutzerAufrufen(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return geprüft(benutzerAufrufen(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return geprüft(benutzerAufrufen(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* Deutsch 공개 함수의 tatsächlichDaten EL0 umsetzung. 구조체는 SVC에서 wertKopieren·검증한다. */
int endpunktErstellen(int adresseFamilie,int kommunikationBetriebsart,int übertragungProtokoll) {
    return geprüft(benutzerAufrufen(32,adresseFamilie,kommunikationBetriebsart,übertragungProtokoll,0,0,0));
}
int adresseZuordnen(int endpunkt,const struct NetzbuchseAdresse *adresse,netzbuchseAdresseLängeTyp Länge) {
    return geprüft(benutzerAufrufen(33,endpunkt,(uintptr_t)adresse,Länge,0,0,0));
}
intptr_t datagrammDatenSenden(int endpunkt,const void *Daten,size_t elementeintragAnzahl,int auswahlWert,const struct NetzbuchseAdresse *adresse,netzbuchseAdresseLängeTyp Länge) {
    return geprüft(benutzerAufrufen(34,endpunkt,(uintptr_t)Daten,elementeintragAnzahl,auswahlWert,(uintptr_t)adresse,Länge));
}
intptr_t datagrammDatenEmpfangen(int endpunkt,void *Daten,size_t elementeintragAnzahl,int auswahlWert,struct NetzbuchseAdresse *adresse,netzbuchseAdresseLängeTyp *Länge) {
    return geprüft(benutzerAufrufen(35,endpunkt,(uintptr_t)Daten,elementeintragAnzahl,auswahlWert,(uintptr_t)adresse,(uintptr_t)Länge));
}
int netzbuchseAdresseLesen(int endpunkt,struct NetzbuchseAdresse *adresse,netzbuchseAdresseLängeTyp *Länge) {
    return geprüft(benutzerAufrufen(36,endpunkt,(uintptr_t)adresse,(uintptr_t)Länge,0,0,0));
}
int netzwerkVerbinden(int endpunkt,const struct NetzbuchseAdresse *adresse,netzbuchseAdresseLängeTyp Länge) {
    return geprüft(benutzerAufrufen(37,endpunkt,(uintptr_t)adresse,Länge,0,0,0));
}
int fürNetzwerkVerbindungWarten(int endpunkt,int wartendAnzahl) {
    return geprüft(benutzerAufrufen(38,endpunkt,wartendAnzahl,0,0,0,0));
}
int netzwerkVerbindungAnnehmen(int endpunkt,struct NetzbuchseAdresse *adresse,netzbuchseAdresseLängeTyp *Länge) {
    return geprüft(benutzerAufrufen(39,endpunkt,(uintptr_t)adresse,(uintptr_t)Länge,0,0,0));
}

/* Datei 함수도 독립된 Deutsch Funktion 심볼로 제공한다. */
int dateiÖffnen(const char *pfad,int methodeBetriebsart,...) { return geprüft(benutzerAufrufen(3,(uintptr_t)pfad,methodeBetriebsart,0,0,0,0)); }
einAusgabeErgebnisTyp dateiDatenLesen(int Datei,void *Daten,size_t elementeintragAnzahl) { return geprüft(benutzerAufrufen(2,Datei,(uintptr_t)Daten,elementeintragAnzahl,0,0,0)); }
einAusgabeErgebnisTyp dateiDatenSchreiben(int Datei,const void *Daten,size_t elementeintragAnzahl) { return geprüft(benutzerAufrufen(1,Datei,(uintptr_t)Daten,elementeintragAnzahl,0,0,0)); }
int dateiSchließen(int Datei) { return geprüft(benutzerAufrufen(4,Datei,0,0,0,0,0)); }
dateiVersatzwertTyp dateiPositionieren(int Datei,dateiVersatzwertTyp entfernungWert,int projektWurzel) { return geprüft(benutzerAufrufen(5,Datei,entfernungWert,projektWurzel,0,0,0)); }
int dateiEintragNameEntfernen(const char *pfad) { return geprüft(benutzerAufrufen(11,(uintptr_t)pfad,0,0,0,0,0)); }
int dateiLängeSetzen(int Datei,dateiVersatzwertTyp größe) { return geprüft(benutzerAufrufen(10,Datei,größe,0,0,0,0)); }
int bestätigenDateiSpeichergerät(int Datei) { return geprüft(benutzerAufrufen(12,Datei,0,0,0,0,0)); }
int dateiGröße(int Datei) { return geprüft(benutzerAufrufen(9,Datei,0,0,0,0,0)); }
