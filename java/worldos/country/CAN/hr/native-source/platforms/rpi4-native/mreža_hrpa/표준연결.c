#include "string.h"
size_t strlen(const char *niz_podaci) { const char *podaci_položaj = niz_podaci; while (*podaci_položaj) podaci_položaj++; return podaci_položaj - niz_podaci; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t artikl_COUNT) { const unsigned char *koordinata_x = 첫째값, *세로좌표 = SECOND_VALUE; while (artikl_COUNT--) { if (*koordinata_x != *세로좌표) return (int)*koordinata_x - *세로좌표; koordinata_x++; 세로좌표++; } return 0; }
void *memmove(void *odredište_podaci, const void *niz_podaci, size_t artikl_COUNT) { unsigned char *koordinata_x = odredište_podaci; const unsigned char *세로좌표 = niz_podaci; if (koordinata_x < 세로좌표) { for (size_t 순번 = 0; 순번 < artikl_COUNT; 순번++) koordinata_x[순번] = 세로좌표[순번]; } else { while (artikl_COUNT) { artikl_COUNT--; koordinata_x[artikl_COUNT] = 세로좌표[artikl_COUNT]; } } return odredište_podaci; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t artikl_COUNT) { while (artikl_COUNT--) { unsigned char koordinata_x = *첫째값++, 세로좌표 = *SECOND_VALUE++; if (koordinata_x != 세로좌표) return (int)koordinata_x-세로좌표; if (!koordinata_x) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *niz_podaci, char **završiti_razgovor_pomak, int podloga_VALUE) {
    const char *START_pomak = niz_podaci; unsigned long VALUE = 0; int šifriranje_VALUE = 1, 하나라도 = 0;
    while (*niz_podaci == ' ' || (*niz_podaci >= 9 && *niz_podaci <= 13)) niz_podaci++;
    if (*niz_podaci == '-' || *niz_podaci == '+') { if (*niz_podaci == '-') šifriranje_VALUE = -1; niz_podaci++; }
    if (podloga_VALUE == 0) podloga_VALUE = 10;
    while (*niz_podaci >= '0' && *niz_podaci <= '9' && *niz_podaci - '0' < podloga_VALUE) {
        unsigned znamenka_VALUE = *niz_podaci++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - znamenka_VALUE) / (unsigned)podloga_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * podloga_VALUE + znamenka_VALUE;
    }
    if (završiti_razgovor_pomak) *završiti_razgovor_pomak = (char *)(하나라도 ? niz_podaci : START_pomak); return šifriranje_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *niz_podaci) { return (int)strtol(niz_podaci, 0, 10); }
