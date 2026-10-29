#include "string.h"
size_t strlen(const char *testun_data) { const char *data_safle = testun_data; while (*data_safle) data_safle++; return data_safle - testun_data; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t eitem_COUNT) { const unsigned char *cyfesuryn_x = 첫째값, *Y_cyfesuryn = SECOND_VALUE; while (eitem_COUNT--) { if (*cyfesuryn_x != *Y_cyfesuryn) return (int)*cyfesuryn_x - *Y_cyfesuryn; cyfesuryn_x++; Y_cyfesuryn++; } return 0; }
void *memmove(void *cyrchfan_data, const void *testun_data, size_t eitem_COUNT) { unsigned char *cyfesuryn_x = cyrchfan_data; const unsigned char *Y_cyfesuryn = testun_data; if (cyfesuryn_x < Y_cyfesuryn) { for (size_t 순번 = 0; 순번 < eitem_COUNT; 순번++) cyfesuryn_x[순번] = Y_cyfesuryn[순번]; } else { while (eitem_COUNT) { eitem_COUNT--; cyfesuryn_x[eitem_COUNT] = Y_cyfesuryn[eitem_COUNT]; } } return cyrchfan_data; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t eitem_COUNT) { while (eitem_COUNT--) { unsigned char cyfesuryn_x = *첫째값++, Y_cyfesuryn = *SECOND_VALUE++; if (cyfesuryn_x != Y_cyfesuryn) return (int)cyfesuryn_x-Y_cyfesuryn; if (!cyfesuryn_x) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *testun_data, char **gorffen_OFFSET, int Cefndir_VALUE) {
    const char *START_OFFSET = testun_data; unsigned long VALUE = 0; int amgodio_VALUE = 1, 하나라도 = 0;
    while (*testun_data == ' ' || (*testun_data >= 9 && *testun_data <= 13)) testun_data++;
    if (*testun_data == '-' || *testun_data == '+') { if (*testun_data == '-') amgodio_VALUE = -1; testun_data++; }
    if (Cefndir_VALUE == 0) Cefndir_VALUE = 10;
    while (*testun_data >= '0' && *testun_data <= '9' && *testun_data - '0' < Cefndir_VALUE) {
        unsigned digid_VALUE = *testun_data++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - digid_VALUE) / (unsigned)Cefndir_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * Cefndir_VALUE + digid_VALUE;
    }
    if (gorffen_OFFSET) *gorffen_OFFSET = (char *)(하나라도 ? testun_data : START_OFFSET); return amgodio_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *testun_data) { return (int)strtol(testun_data, 0, 10); }
