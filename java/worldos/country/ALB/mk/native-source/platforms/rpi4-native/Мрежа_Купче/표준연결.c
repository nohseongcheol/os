#include "string.h"
size_t strlen(const char *низа_податоци) { const char *податоци_позиционирање = низа_податоци; while (*податоци_позиционирање) податоци_позиционирање++; return податоци_позиционирање - низа_податоци; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t ставка_COUNT) { const unsigned char *координата_х = 첫째값, *세로좌표 = SECOND_VALUE; while (ставка_COUNT--) { if (*координата_х != *세로좌표) return (int)*координата_х - *세로좌표; координата_х++; 세로좌표++; } return 0; }
void *memmove(void *одредиште_податоци, const void *низа_податоци, size_t ставка_COUNT) { unsigned char *координата_х = одредиште_податоци; const unsigned char *세로좌표 = низа_податоци; if (координата_х < 세로좌표) { for (size_t 순번 = 0; 순번 < ставка_COUNT; 순번++) координата_х[순번] = 세로좌표[순번]; } else { while (ставка_COUNT) { ставка_COUNT--; координата_х[ставка_COUNT] = 세로좌표[ставка_COUNT]; } } return одредиште_податоци; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t ставка_COUNT) { while (ставка_COUNT--) { unsigned char координата_х = *첫째값++, 세로좌표 = *SECOND_VALUE++; if (координата_х != 세로좌표) return (int)координата_х-세로좌표; if (!координата_х) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *низа_податоци, char **крај_OFFSET, int тапет_VALUE) {
    const char *Start_OFFSET = низа_податоци; unsigned long VALUE = 0; int кодирање_VALUE = 1, 하나라도 = 0;
    while (*низа_податоци == ' ' || (*низа_податоци >= 9 && *низа_податоци <= 13)) низа_податоци++;
    if (*низа_податоци == '-' || *низа_податоци == '+') { if (*низа_податоци == '-') кодирање_VALUE = -1; низа_податоци++; }
    if (тапет_VALUE == 0) тапет_VALUE = 10;
    while (*низа_податоци >= '0' && *низа_податоци <= '9' && *низа_податоци - '0' < тапет_VALUE) {
        unsigned цифра_VALUE = *низа_податоци++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - цифра_VALUE) / (unsigned)тапет_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * тапет_VALUE + цифра_VALUE;
    }
    if (крај_OFFSET) *крај_OFFSET = (char *)(하나라도 ? низа_податоци : Start_OFFSET); return кодирање_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *низа_податоци) { return (int)strtol(низа_податоци, 0, 10); }
