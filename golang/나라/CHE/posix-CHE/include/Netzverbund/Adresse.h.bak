#ifndef _include_Netzverbund_Adresse
#define _include_Netzverbund_Adresse

#include <Ganzzahltypen.h>
#include <System/socket.h>

typedef uint32_t Typ_des_Netzverbundadresswerts;
typedef uint16_t Typ_der_Kommunikationsportnummer;

struct Netzverbundadresse {
    Typ_des_Netzverbundadresswerts Adresswert;
};

struct Netzverbundendpunktadresse {
    Adressfamilientyp Netzverbundadressfamilie;
    Typ_der_Kommunikationsportnummer Kommunikationsportnummer;
    struct Netzverbundadresse Netzverbundadressinhalt;
    unsigned char Adressauffüllung[8];
};

#define Netzverbundgrundprotokoll 0
#define Benutzerdatagrammprotokoll 17
#define beliebige_lokale_Adresse ((Typ_des_Netzverbundadresswerts)0x00000000U)
#define Rückschleifenadresse ((Typ_des_Netzverbundadresswerts)0x7f000001U)

#endif
