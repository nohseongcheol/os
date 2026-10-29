#include "string.h"
size_t strlen(const char *string_podaci) { const char *podaci_položaj = string_podaci; while (*podaci_položaj) podaci_položaj++; return podaci_položaj - string_podaci; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t stavka_COUNT) { const unsigned char *koordinata_x = 첫째값, *Y_koordinata = SECOND_VALUE; while (stavka_COUNT--) { if (*koordinata_x != *Y_koordinata) return (int)*koordinata_x - *Y_koordinata; koordinata_x++; Y_koordinata++; } return 0; }
void *memmove(void *odredište_podaci, const void *string_podaci, size_t stavka_COUNT) { unsigned char *koordinata_x = odredište_podaci; const unsigned char *Y_koordinata = string_podaci; if (koordinata_x < Y_koordinata) { for (size_t 순번 = 0; 순번 < stavka_COUNT; 순번++) koordinata_x[순번] = Y_koordinata[순번]; } else { while (stavka_COUNT) { stavka_COUNT--; koordinata_x[stavka_COUNT] = Y_koordinata[stavka_COUNT]; } } return odredište_podaci; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t stavka_COUNT) { while (stavka_COUNT--) { unsigned char koordinata_x = *첫째값++, Y_koordinata = *SECOND_VALUE++; if (koordinata_x != Y_koordinata) return (int)koordinata_x-Y_koordinata; if (!koordinata_x) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *string_podaci, char **završiti_Pomak, int poster_VALUE) {
    const char *START_Pomak = string_podaci; unsigned long VALUE = 0; int kodiranje_VALUE = 1, 하나라도 = 0;
    while (*string_podaci == ' ' || (*string_podaci >= 9 && *string_podaci <= 13)) string_podaci++;
    if (*string_podaci == '-' || *string_podaci == '+') { if (*string_podaci == '-') kodiranje_VALUE = -1; string_podaci++; }
    if (poster_VALUE == 0) poster_VALUE = 10;
    while (*string_podaci >= '0' && *string_podaci <= '9' && *string_podaci - '0' < poster_VALUE) {
        unsigned cifra_VALUE = *string_podaci++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - cifra_VALUE) / (unsigned)poster_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * poster_VALUE + cifra_VALUE;
    }
    if (završiti_Pomak) *završiti_Pomak = (char *)(하나라도 ? string_podaci : START_Pomak); return kodiranje_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *string_podaci) { return (int)strtol(string_podaci, 0, 10); }
