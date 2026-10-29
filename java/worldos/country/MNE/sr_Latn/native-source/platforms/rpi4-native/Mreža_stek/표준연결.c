#include "string.h"
size_t strlen(const char *niska_podaci) { const char *podaci_pozicija = niska_podaci; while (*podaci_pozicija) podaci_pozicija++; return podaci_pozicija - niska_podaci; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t stavka_COUNT) { const unsigned char *x_koordinata = 첫째값, *세로좌표 = SECOND_VALUE; while (stavka_COUNT--) { if (*x_koordinata != *세로좌표) return (int)*x_koordinata - *세로좌표; x_koordinata++; 세로좌표++; } return 0; }
void *memmove(void *odredište_podaci, const void *niska_podaci, size_t stavka_COUNT) { unsigned char *x_koordinata = odredište_podaci; const unsigned char *세로좌표 = niska_podaci; if (x_koordinata < 세로좌표) { for (size_t 순번 = 0; 순번 < stavka_COUNT; 순번++) x_koordinata[순번] = 세로좌표[순번]; } else { while (stavka_COUNT) { stavka_COUNT--; x_koordinata[stavka_COUNT] = 세로좌표[stavka_COUNT]; } } return odredište_podaci; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t stavka_COUNT) { while (stavka_COUNT--) { unsigned char x_koordinata = *첫째값++, 세로좌표 = *SECOND_VALUE++; if (x_koordinata != 세로좌표) return (int)x_koordinata-세로좌표; if (!x_koordinata) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *niska_podaci, char **završiti_razgovor_Pomak, int poster_VALUE) {
    const char *START_Pomak = niska_podaci; unsigned long VALUE = 0; int kodiranje_VALUE = 1, 하나라도 = 0;
    while (*niska_podaci == ' ' || (*niska_podaci >= 9 && *niska_podaci <= 13)) niska_podaci++;
    if (*niska_podaci == '-' || *niska_podaci == '+') { if (*niska_podaci == '-') kodiranje_VALUE = -1; niska_podaci++; }
    if (poster_VALUE == 0) poster_VALUE = 10;
    while (*niska_podaci >= '0' && *niska_podaci <= '9' && *niska_podaci - '0' < poster_VALUE) {
        unsigned cifra_VALUE = *niska_podaci++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - cifra_VALUE) / (unsigned)poster_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * poster_VALUE + cifra_VALUE;
    }
    if (završiti_razgovor_Pomak) *završiti_razgovor_Pomak = (char *)(하나라도 ? niska_podaci : START_Pomak); return kodiranje_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *niska_podaci) { return (int)strtol(niska_podaci, 0, 10); }
