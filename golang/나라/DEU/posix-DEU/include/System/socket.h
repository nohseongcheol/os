/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _include_System_socket
#define _include_System_socket

#include <Grunddefinitionen.h>
#include <System/Datentypen.h>

typedef unsigned short Adressfamilientyp;

struct Kommunikationsendpunktadresse {
    Adressfamilientyp Endpunktadressfamilie;
    char Adressdaten[14];
};

#define nicht_festgelegte_Adressfamilie 0
#define Netzverbundadressfamilienkennung 2
#define Netzverbundprotokollfamilie Netzverbundadressfamilienkennung

#define Datenstromendpunkt 1
#define Datagrammendpunkt 2

#define Empfang_beenden 0
#define Senden_beenden 1
#define beide_Richtungen_beenden 2

#ifdef __cplusplus
extern "C" {
#endif
int Kommunikationsendpunkt_anlegen(int domain, int type, int protocol);
int lokale_Adresse_zuordnen(int Dateideskriptor, const struct Kommunikationsendpunktadresse *address, Adresslängentyp address_len);
int Gegenstelle_verbinden(int Dateideskriptor, const struct Kommunikationsendpunktadresse *address, Adresslängentyp address_len);
int Verbindungsannahme_vorbereiten(int Dateideskriptor, int backlog);
int Verbindung_annehmen(int Dateideskriptor, struct Kommunikationsendpunktadresse *address, Adresslängentyp *address_len);
int lokale_Endpunktadresse_ermitteln(int Dateideskriptor, struct Kommunikationsendpunktadresse *address, Adresslängentyp *address_len);
int Gegenstellenadresse_ermitteln(int Dateideskriptor, struct Kommunikationsendpunktadresse *address, Adresslängentyp *address_len);
ssize_t senden(int Dateideskriptor, const void *Übertragungspuffer_2, size_t Länge, int flags);
ssize_t empfangen(int Dateideskriptor, void *Übertragungspuffer_2, size_t Länge, int flags);
ssize_t an_Zieladresse_senden(int Dateideskriptor, const void *message, size_t Länge, int flags,
               const struct Kommunikationsendpunktadresse *dest_addr, Adresslängentyp dest_len);
ssize_t mit_Absenderadresse_empfangen(int Dateideskriptor, void *Übertragungspuffer_2, size_t Länge, int flags,
                 struct Kommunikationsendpunktadresse *address, Adresslängentyp *address_len);
int Übertragungsrichtung_schließen(int Dateideskriptor, int how);
int Endpunktoption_setzen(int Dateideskriptor, int level, int option_name,
               const void *option_value, Adresslängentyp option_len);
#ifdef __cplusplus
}
#endif

#endif
