/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <Netzadressumwandlung/Bytereihenfolge.h>
#include <System/syscall.h>
#include <System/socket.h>

enum { SYS_socketcall = 102 };
enum {
    SC_Kommunikationsendpunkt_anlegen = 1, SC_lokale_Adresse_zuordnen = 2, SC_Gegenstelle_verbinden = 3, SC_Verbindungsannahme_vorbereiten = 4,
    SC_Verbindung_annehmen = 5, SC_lokale_Endpunktadresse_ermitteln = 6, SC_Gegenstellenadresse_ermitteln = 7,
    SC_senden = 9, SC_empfangen = 10, SC_an_Zieladresse_senden = 11, SC_mit_Absenderadresse_empfangen = 12,
    SC_Übertragungsrichtung_schließen = 13, SC_Endpunktoption_setzen = 14
};

static long socket_call(long call, unsigned long *Argumente)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)Argumente, 0, 0, 0, 0));
}

uint16_t _16_Bit_in_Netzreihenfolge(uint16_t Wert) { return (uint16_t)((Wert << 8) | (Wert >> 8)); }
uint16_t _16_Bit_in_Rechnerreihenfolge(uint16_t Wert) { return _16_Bit_in_Netzreihenfolge(Wert); }
uint32_t _32_Bit_in_Netzreihenfolge(uint32_t Wert)
{
    return ((Wert & 0x000000ffU) << 24) | ((Wert & 0x0000ff00U) << 8) |
           ((Wert & 0x00ff0000U) >> 8) | ((Wert & 0xff000000U) >> 24);
}
uint32_t _32_Bit_in_Rechnerreihenfolge(uint32_t Wert) { return _32_Bit_in_Netzreihenfolge(Wert); }

int Kommunikationsendpunkt_anlegen(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_Kommunikationsendpunkt_anlegen, a);
}

int lokale_Adresse_zuordnen(int Dateideskriptor, const struct Kommunikationsendpunktadresse *address, Adresslängentyp Länge)
{
    unsigned long a[3] = {(unsigned long)Dateideskriptor, (unsigned long)address, Länge};
    return (int)socket_call(SC_lokale_Adresse_zuordnen, a);
}

int Gegenstelle_verbinden(int Dateideskriptor, const struct Kommunikationsendpunktadresse *address, Adresslängentyp Länge)
{
    unsigned long a[3] = {(unsigned long)Dateideskriptor, (unsigned long)address, Länge};
    return (int)socket_call(SC_Gegenstelle_verbinden, a);
}

int Verbindungsannahme_vorbereiten(int Dateideskriptor, int backlog)
{
    unsigned long a[2] = {(unsigned long)Dateideskriptor, (unsigned long)backlog};
    return (int)socket_call(SC_Verbindungsannahme_vorbereiten, a);
}

int Verbindung_annehmen(int Dateideskriptor, struct Kommunikationsendpunktadresse *address, Adresslängentyp *Länge)
{
    unsigned long a[3] = {(unsigned long)Dateideskriptor, (unsigned long)address, (unsigned long)Länge};
    return (int)socket_call(SC_Verbindung_annehmen, a);
}

int lokale_Endpunktadresse_ermitteln(int Dateideskriptor, struct Kommunikationsendpunktadresse *address, Adresslängentyp *Länge)
{
    unsigned long a[3] = {(unsigned long)Dateideskriptor, (unsigned long)address, (unsigned long)Länge};
    return (int)socket_call(SC_lokale_Endpunktadresse_ermitteln, a);
}

int Gegenstellenadresse_ermitteln(int Dateideskriptor, struct Kommunikationsendpunktadresse *address, Adresslängentyp *Länge)
{
    unsigned long a[3] = {(unsigned long)Dateideskriptor, (unsigned long)address, (unsigned long)Länge};
    return (int)socket_call(SC_Gegenstellenadresse_ermitteln, a);
}

ssize_t senden(int Dateideskriptor, const void *Übertragungspuffer_2, size_t Länge, int flags)
{
    unsigned long a[4] = {(unsigned long)Dateideskriptor, (unsigned long)Übertragungspuffer_2, Länge, (unsigned long)flags};
    return (ssize_t)socket_call(SC_senden, a);
}

ssize_t empfangen(int Dateideskriptor, void *Übertragungspuffer_2, size_t Länge, int flags)
{
    unsigned long a[4] = {(unsigned long)Dateideskriptor, (unsigned long)Übertragungspuffer_2, Länge, (unsigned long)flags};
    return (ssize_t)socket_call(SC_empfangen, a);
}

ssize_t an_Zieladresse_senden(int Dateideskriptor, const void *Übertragungspuffer_2, size_t Länge, int flags,
               const struct Kommunikationsendpunktadresse *address, Adresslängentyp address_length)
{
    unsigned long a[6] = {(unsigned long)Dateideskriptor, (unsigned long)Übertragungspuffer_2, Länge,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_an_Zieladresse_senden, a);
}

ssize_t mit_Absenderadresse_empfangen(int Dateideskriptor, void *Übertragungspuffer_2, size_t Länge, int flags,
                 struct Kommunikationsendpunktadresse *address, Adresslängentyp *address_length)
{
    unsigned long a[6] = {(unsigned long)Dateideskriptor, (unsigned long)Übertragungspuffer_2, Länge,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_mit_Absenderadresse_empfangen, a);
}

int Übertragungsrichtung_schließen(int Dateideskriptor, int how)
{
    unsigned long a[2] = {(unsigned long)Dateideskriptor, (unsigned long)how};
    return (int)socket_call(SC_Übertragungsrichtung_schließen, a);
}

int Endpunktoption_setzen(int Dateideskriptor, int level, int option_name,
               const void *option_value, Adresslängentyp option_len)
{
    unsigned long a[5] = {(unsigned long)Dateideskriptor, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_Endpunktoption_setzen, a);
}
