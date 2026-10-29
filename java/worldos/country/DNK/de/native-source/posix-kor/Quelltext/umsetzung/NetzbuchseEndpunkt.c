#include <NetzwerkABI.h>
#include <errno.h>
#include "AufrufVorgangGrenzstelle.h"

int socket(int adresseSchema, int netzwerkArt, int vertragNummer) {
    return aufrufErgebnis(jkoros_syscall(41, adresseSchema, netzwerkArt, vertragNummer, 0, 0));
}
int bind(int dateiDeskriptor, const struct sockaddr *adresse, socklen_t adresseLänge) {
    return aufrufErgebnis(jkoros_syscall(42, dateiDeskriptor, (int)adresse, adresseLänge, 0, 0));
}
ssize_t sendto(int dateiDeskriptor, const void *Daten, size_t byteAnzahl, int einstellungen,
               const struct sockaddr *adresse, socklen_t adresseLänge) {
    int anfrage[2] = {(int)adresse, adresseLänge};
    return aufrufErgebnis(jkoros_syscall(43, dateiDeskriptor, (int)Daten, byteAnzahl, einstellungen, (int)anfrage));
}
ssize_t recvfrom(int dateiDeskriptor, void *Daten, size_t byteAnzahl, int einstellungen,
                 struct sockaddr *adresse, socklen_t *adresseLänge) {
    int anfrage[2] = {(int)adresse, (int)adresseLänge};
    return aufrufErgebnis(jkoros_syscall(44, dateiDeskriptor, (int)Daten, byteAnzahl, einstellungen, (int)anfrage));
}
int getsockname(int dateiDeskriptor, struct sockaddr *adresse, socklen_t *adresseLänge) {
    return aufrufErgebnis(jkoros_syscall(45, dateiDeskriptor, (int)adresse, (int)adresseLänge, 0, 0));
}
int setsockopt(int dateiDeskriptor, int schichtWert, int einstellungenName, const void *Wert, socklen_t wertLänge) {
    if (schichtWert != SOL_SOCKET || einstellungenName != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!Wert) { errno = EFAULT; return -1; }
    if (wertLänge != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *zeitWert = Wert;
    if (zeitWert->tv_sec < 0 || zeitWert->tv_sec > 2 || zeitWert->tv_usec < 0 || zeitWert->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int millisekunden = zeitWert->tv_sec * 1000 + (zeitWert->tv_usec + 999) / 1000;
    return aufrufErgebnis(jkoros_syscall(46, dateiDeskriptor, millisekunden, 0, 0, 0));
}
uint16_t htons(uint16_t Wert) { return (Wert << 8) | (Wert >> 8); }
uint16_t ntohs(uint16_t Wert) { return htons(Wert); }
uint32_t htonl(uint32_t Wert) {
    return (Wert << 24) | ((Wert << 8) & 0xff0000U) | ((Wert >> 8) & 0xff00U) | (Wert >> 24);
}
uint32_t ntohl(uint32_t Wert) { return htonl(Wert); }
int inet_pton(int adresseSchema, const char *Zeichenkette, void *adresse) {
    if (adresseSchema != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!Zeichenkette || !adresse) { errno = EFAULT; return -1; }
    unsigned char vorläufigWert[4];
    for (int platzEintrag = 0; platzEintrag < 4; platzEintrag++) {
        int Wert = 0, ziffern = 0;
        const char *ausführenVorgang = Zeichenkette;
        while (*Zeichenkette >= '0' && *Zeichenkette <= '9') {
            if (++ziffern > 3) return 0;
            Wert = Wert * 10 + *Zeichenkette++ - '0';
        }
        if (!ziffern || Wert > 255 || (ziffern > 1 && *ausführenVorgang == '0')) return 0;
        vorläufigWert[platzEintrag] = Wert;
        if (platzEintrag < 3) { if (*Zeichenkette++ != '.') return 0; }
        else if (*Zeichenkette) return 0;
    }
    for (int platzEintrag = 0; platzEintrag < 4; platzEintrag++) ((unsigned char *)adresse)[platzEintrag] = vorläufigWert[platzEintrag];
    return 1;
}
const char *inet_ntop(int adresseSchema, const void *adresse, char *Zeichenkette, socklen_t kapazitätWert) {
    if (adresseSchema != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!adresse || !Zeichenkette) { errno = EFAULT; return 0; }
    const unsigned char *Zahl = adresse;
    char vorläufigWert[16]; unsigned int Länge = 0;
    for (int platzEintrag = 0; platzEintrag < 4; platzEintrag++) {
        unsigned int Wert = Zahl[platzEintrag];
        if (Wert >= 100) vorläufigWert[Länge++] = '0' + Wert / 100;
        if (Wert >= 10) vorläufigWert[Länge++] = '0' + Wert / 10 % 10;
        vorläufigWert[Länge++] = '0' + Wert % 10;
        if (platzEintrag < 3) vorläufigWert[Länge++] = '.';
    }
    vorläufigWert[Länge++] = 0;
    if (kapazitätWert < Länge) { errno = ENOSPC; return 0; }
    for (unsigned int platzEintrag = 0; platzEintrag < Länge; platzEintrag++) Zeichenkette[platzEintrag] = vorläufigWert[platzEintrag];
    return Zeichenkette;
}
