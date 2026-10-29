#include "string.h"
size_t strlen(const char *teaghrán_sonraí) { const char *sonraí_suíomh = teaghrán_sonraí; while (*sonraí_suíomh) sonraí_suíomh++; return sonraí_suíomh - teaghrán_sonraí; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t mír_COUNT) { const unsigned char *x_chomhordanáid = 첫째값, *세로좌표 = SECOND_VALUE; while (mír_COUNT--) { if (*x_chomhordanáid != *세로좌표) return (int)*x_chomhordanáid - *세로좌표; x_chomhordanáid++; 세로좌표++; } return 0; }
void *memmove(void *sprioc_sonraí, const void *teaghrán_sonraí, size_t mír_COUNT) { unsigned char *x_chomhordanáid = sprioc_sonraí; const unsigned char *세로좌표 = teaghrán_sonraí; if (x_chomhordanáid < 세로좌표) { for (size_t 순번 = 0; 순번 < mír_COUNT; 순번++) x_chomhordanáid[순번] = 세로좌표[순번]; } else { while (mír_COUNT) { mír_COUNT--; x_chomhordanáid[mír_COUNT] = 세로좌표[mír_COUNT]; } } return sprioc_sonraí; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t mír_COUNT) { while (mír_COUNT--) { unsigned char x_chomhordanáid = *첫째값++, 세로좌표 = *SECOND_VALUE++; if (x_chomhordanáid != 세로좌표) return (int)x_chomhordanáid-세로좌표; if (!x_chomhordanáid) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *teaghrán_sonraí, char **cuir_deireadh_le_OFFSET, int Cúlra_VALUE) {
    const char *Start_OFFSET = teaghrán_sonraí; unsigned long VALUE = 0; int ionchódú_VALUE = 1, 하나라도 = 0;
    while (*teaghrán_sonraí == ' ' || (*teaghrán_sonraí >= 9 && *teaghrán_sonraí <= 13)) teaghrán_sonraí++;
    if (*teaghrán_sonraí == '-' || *teaghrán_sonraí == '+') { if (*teaghrán_sonraí == '-') ionchódú_VALUE = -1; teaghrán_sonraí++; }
    if (Cúlra_VALUE == 0) Cúlra_VALUE = 10;
    while (*teaghrán_sonraí >= '0' && *teaghrán_sonraí <= '9' && *teaghrán_sonraí - '0' < Cúlra_VALUE) {
        unsigned digit_VALUE = *teaghrán_sonraí++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - digit_VALUE) / (unsigned)Cúlra_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * Cúlra_VALUE + digit_VALUE;
    }
    if (cuir_deireadh_le_OFFSET) *cuir_deireadh_le_OFFSET = (char *)(하나라도 ? teaghrán_sonraí : Start_OFFSET); return ionchódú_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *teaghrán_sonraí) { return (int)strtol(teaghrán_sonraí, 0, 10); }
