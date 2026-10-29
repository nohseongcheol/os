#include "string.h"
size_t strlen(const char *string_andmed) { const char *andmed_ametikoht = string_andmed; while (*andmed_ametikoht) andmed_ametikoht++; return andmed_ametikoht - string_andmed; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t kaup_COUNT) { const unsigned char *가로좌표 = 첫째값, *세로좌표 = SECOND_VALUE; while (kaup_COUNT--) { if (*가로좌표 != *세로좌표) return (int)*가로좌표 - *세로좌표; 가로좌표++; 세로좌표++; } return 0; }
void *memmove(void *sihtkoht_andmed, const void *string_andmed, size_t kaup_COUNT) { unsigned char *가로좌표 = sihtkoht_andmed; const unsigned char *세로좌표 = string_andmed; if (가로좌표 < 세로좌표) { for (size_t 순번 = 0; 순번 < kaup_COUNT; 순번++) 가로좌표[순번] = 세로좌표[순번]; } else { while (kaup_COUNT) { kaup_COUNT--; 가로좌표[kaup_COUNT] = 세로좌표[kaup_COUNT]; } } return sihtkoht_andmed; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t kaup_COUNT) { while (kaup_COUNT--) { unsigned char 가로좌표 = *첫째값++, 세로좌표 = *SECOND_VALUE++; if (가로좌표 != 세로좌표) return (int)가로좌표-세로좌표; if (!가로좌표) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *string_andmed, char **lõpeta_kõne_nihe, int taust_VALUE) {
    const char *START_nihe = string_andmed; unsigned long VALUE = 0; int kodeerimine_VALUE = 1, 하나라도 = 0;
    while (*string_andmed == ' ' || (*string_andmed >= 9 && *string_andmed <= 13)) string_andmed++;
    if (*string_andmed == '-' || *string_andmed == '+') { if (*string_andmed == '-') kodeerimine_VALUE = -1; string_andmed++; }
    if (taust_VALUE == 0) taust_VALUE = 10;
    while (*string_andmed >= '0' && *string_andmed <= '9' && *string_andmed - '0' < taust_VALUE) {
        unsigned number_VALUE = *string_andmed++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - number_VALUE) / (unsigned)taust_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * taust_VALUE + number_VALUE;
    }
    if (lõpeta_kõne_nihe) *lõpeta_kõne_nihe = (char *)(하나라도 ? string_andmed : START_nihe); return kodeerimine_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *string_andmed) { return (int)strtol(string_andmed, 0, 10); }
