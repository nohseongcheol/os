#include "../benennung/maschineBindenNamen.h"
#include "aufrufen.h"
typedef void (*initialisiererMethode)(void);
extern initialisiererMethode __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int benutzerProgrammStarten(int);
int benutzerStarten(int weitergeleitetWert) {
    for (initialisiererMethode *datenPosition = __init_array_start; datenPosition < __init_array_end; datenPosition++) (*datenPosition)();
    int ergebnis = benutzerProgrammStarten(weitergeleitetWert);
    for (initialisiererMethode *datenPosition = __fini_array_end; datenPosition != __fini_array_start;) (*--datenPosition)();
    return ergebnis;
}
void *memset(void *datenPosition, int Wert, size_t eintragAnzahl) { unsigned char *zielDaten = datenPosition; while (eintragAnzahl--) *zielDaten++ = Wert; return datenPosition; }
void *memcpy(void *zielDaten, const void *zeichenketteDaten, size_t eintragAnzahl) { unsigned char *ersterWert = zielDaten; const unsigned char *zweiterWert = zeichenketteDaten; while (eintragAnzahl--) *ersterWert++ = *zweiterWert++; return zielDaten; }
