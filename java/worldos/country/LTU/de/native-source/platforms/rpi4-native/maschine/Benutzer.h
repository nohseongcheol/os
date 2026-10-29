#ifndef systemnahBenutzerKopf
#define systemnahBenutzerKopf
#include <stdint.h>
#include <stddef.h>
#define benutzerBasis 0x02000000ul
#define benutzerAbbildEnde 0x02c00000ul
#define benutzerSpeicherhaldeEnde 0x02ed0000ul
#define benutzerStapelAdresse 0x02f00000ul
#define benutzerEnde 0x03000000ul
#define benutzerSeiteAnzahl ((benutzerEnde - benutzerBasis) / 4096ul)
#define benutzerAusführdateiFehler (-8)
#define benutzerDatenFehler (-1001)
#define benutzerAusführungFehler (-1002)
#define benutzerUngültigBefehlswort (-1003)
#define benutzerZeitüberschreitung (-1004)
#define benutzerUnterbrochen (-1005)
typedef struct { uint64_t datenRegister[31], befehlPosition, statuswertKode, stapelAdresse; } benutzerRahmen;
void benutzerSystemInitialisierungsvorgang(void);
int benutzerAusnahme(benutzerRahmen *, unsigned);
int benutzerValidierenELF(const unsigned char *, size_t);
uintptr_t platineBenutzerAusführenVorgang(uintptr_t);
uintptr_t platineBenutzerValidieren(void);
uintptr_t platineBenutzerSteuerung(uintptr_t);
uint32_t benutzerStatuswertLesen(unsigned, unsigned);
#endif
