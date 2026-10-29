#include "string.h"
size_t strlen(const char *streng_data) { const char *data_plassere = streng_data; while (*data_plassere) data_plassere++; return data_plassere - streng_data; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t vare_COUNT) { const unsigned char *x_koordinat = 첫째값, *Y_koordinat = SECOND_VALUE; while (vare_COUNT--) { if (*x_koordinat != *Y_koordinat) return (int)*x_koordinat - *Y_koordinat; x_koordinat++; Y_koordinat++; } return 0; }
void *memmove(void *mål_data, const void *streng_data, size_t vare_COUNT) { unsigned char *x_koordinat = mål_data; const unsigned char *Y_koordinat = streng_data; if (x_koordinat < Y_koordinat) { for (size_t 순번 = 0; 순번 < vare_COUNT; 순번++) x_koordinat[순번] = Y_koordinat[순번]; } else { while (vare_COUNT) { vare_COUNT--; x_koordinat[vare_COUNT] = Y_koordinat[vare_COUNT]; } } return mål_data; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t vare_COUNT) { while (vare_COUNT--) { unsigned char x_koordinat = *첫째값++, Y_koordinat = *SECOND_VALUE++; if (x_koordinat != Y_koordinat) return (int)x_koordinat-Y_koordinat; if (!x_koordinat) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *streng_data, char **avslutte_OFFSET, int bakgrunn_VALUE) {
    const char *START_OFFSET = streng_data; unsigned long VALUE = 0; int koding_VALUE = 1, 하나라도 = 0;
    while (*streng_data == ' ' || (*streng_data >= 9 && *streng_data <= 13)) streng_data++;
    if (*streng_data == '-' || *streng_data == '+') { if (*streng_data == '-') koding_VALUE = -1; streng_data++; }
    if (bakgrunn_VALUE == 0) bakgrunn_VALUE = 10;
    while (*streng_data >= '0' && *streng_data <= '9' && *streng_data - '0' < bakgrunn_VALUE) {
        unsigned siffer_VALUE = *streng_data++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - siffer_VALUE) / (unsigned)bakgrunn_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * bakgrunn_VALUE + siffer_VALUE;
    }
    if (avslutte_OFFSET) *avslutte_OFFSET = (char *)(하나라도 ? streng_data : START_OFFSET); return koding_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *streng_data) { return (int)strtol(streng_data, 0, 10); }
