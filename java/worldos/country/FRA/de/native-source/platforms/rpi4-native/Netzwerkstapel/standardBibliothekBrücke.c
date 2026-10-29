#include "string.h"
size_t strlen(const char *zeichenketteDaten) { const char *datenPosition = zeichenketteDaten; while (*datenPosition) datenPosition++; return datenPosition - zeichenketteDaten; }
int memcmp(const void *ersterWert, const void *zweiterWert, size_t elementeintragAnzahl) { const unsigned char *waagerechteKoordinateKoordinate = ersterWert, *senkrechteKoordinateKoordinate = zweiterWert; while (elementeintragAnzahl--) { if (*waagerechteKoordinateKoordinate != *senkrechteKoordinateKoordinate) return (int)*waagerechteKoordinateKoordinate - *senkrechteKoordinateKoordinate; waagerechteKoordinateKoordinate++; senkrechteKoordinateKoordinate++; } return 0; }
void *memmove(void *zielDaten, const void *zeichenketteDaten, size_t elementeintragAnzahl) { unsigned char *waagerechteKoordinateKoordinate = zielDaten; const unsigned char *senkrechteKoordinateKoordinate = zeichenketteDaten; if (waagerechteKoordinateKoordinate < senkrechteKoordinateKoordinate) { for (size_t ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) waagerechteKoordinateKoordinate[ordnungszahlIndex] = senkrechteKoordinateKoordinate[ordnungszahlIndex]; } else { while (elementeintragAnzahl) { elementeintragAnzahl--; waagerechteKoordinateKoordinate[elementeintragAnzahl] = senkrechteKoordinateKoordinate[elementeintragAnzahl]; } } return zielDaten; }
int strncmp(const char *ersterWert, const char *zweiterWert, size_t elementeintragAnzahl) { while (elementeintragAnzahl--) { unsigned char waagerechteKoordinateKoordinate = *ersterWert++, senkrechteKoordinateKoordinate = *zweiterWert++; if (waagerechteKoordinateKoordinate != senkrechteKoordinateKoordinate) return (int)waagerechteKoordinateKoordinate-senkrechteKoordinateKoordinate; if (!waagerechteKoordinateKoordinate) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *zeichenketteDaten, char **endeVersatzwert, int hintergrundWert) {
    const char *versatzwertStarten = zeichenketteDaten; unsigned long Wert = 0; int kodierungWert = 1, beliebigWert = 0;
    while (*zeichenketteDaten == ' ' || (*zeichenketteDaten >= 9 && *zeichenketteDaten <= 13)) zeichenketteDaten++;
    if (*zeichenketteDaten == '-' || *zeichenketteDaten == '+') { if (*zeichenketteDaten == '-') kodierungWert = -1; zeichenketteDaten++; }
    if (hintergrundWert == 0) hintergrundWert = 10;
    while (*zeichenketteDaten >= '0' && *zeichenketteDaten <= '9' && *zeichenketteDaten - '0' < hintergrundWert) {
        unsigned zifferWert = *zeichenketteDaten++ - '0'; beliebigWert = 1;
        if (Wert > (0x7ffffffffffffffful - zifferWert) / (unsigned)hintergrundWert) Wert = 0x7ffffffffffffffful;
        else Wert = Wert * hintergrundWert + zifferWert;
    }
    if (endeVersatzwert) *endeVersatzwert = (char *)(beliebigWert ? zeichenketteDaten : versatzwertStarten); return kodierungWert > 0 ? (long)Wert : -(long)Wert;
}
int atoi(const char *zeichenketteDaten) { return (int)strtol(zeichenketteDaten, 0, 10); }
