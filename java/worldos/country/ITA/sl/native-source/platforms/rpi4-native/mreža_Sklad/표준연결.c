#include "string.h"
size_t strlen(const char *niz_podatki) { const char *podatki_položaj = niz_podatki; while (*podatki_položaj) podatki_položaj++; return podatki_položaj - niz_podatki; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t element_COUNT) { const unsigned char *koordinata_x = 첫째값, *세로좌표 = SECOND_VALUE; while (element_COUNT--) { if (*koordinata_x != *세로좌표) return (int)*koordinata_x - *세로좌표; koordinata_x++; 세로좌표++; } return 0; }
void *memmove(void *cilj_podatki, const void *niz_podatki, size_t element_COUNT) { unsigned char *koordinata_x = cilj_podatki; const unsigned char *세로좌표 = niz_podatki; if (koordinata_x < 세로좌표) { for (size_t 순번 = 0; 순번 < element_COUNT; 순번++) koordinata_x[순번] = 세로좌표[순번]; } else { while (element_COUNT) { element_COUNT--; koordinata_x[element_COUNT] = 세로좌표[element_COUNT]; } } return cilj_podatki; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t element_COUNT) { while (element_COUNT--) { unsigned char koordinata_x = *첫째값++, 세로좌표 = *SECOND_VALUE++; if (koordinata_x != 세로좌표) return (int)koordinata_x-세로좌표; if (!koordinata_x) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *niz_podatki, char **končati_klic_odmik, int Ozadje_VALUE) {
    const char *Start_odmik = niz_podatki; unsigned long VALUE = 0; int kodiranje_VALUE = 1, 하나라도 = 0;
    while (*niz_podatki == ' ' || (*niz_podatki >= 9 && *niz_podatki <= 13)) niz_podatki++;
    if (*niz_podatki == '-' || *niz_podatki == '+') { if (*niz_podatki == '-') kodiranje_VALUE = -1; niz_podatki++; }
    if (Ozadje_VALUE == 0) Ozadje_VALUE = 10;
    while (*niz_podatki >= '0' && *niz_podatki <= '9' && *niz_podatki - '0' < Ozadje_VALUE) {
        unsigned številka_VALUE = *niz_podatki++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - številka_VALUE) / (unsigned)Ozadje_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * Ozadje_VALUE + številka_VALUE;
    }
    if (končati_klic_odmik) *končati_klic_odmik = (char *)(하나라도 ? niz_podatki : Start_odmik); return kodiranje_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *niz_podatki) { return (int)strtol(niz_podatki, 0, 10); }
