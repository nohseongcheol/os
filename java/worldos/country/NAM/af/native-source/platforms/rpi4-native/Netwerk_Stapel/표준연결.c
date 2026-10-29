#include "string.h"
size_t strlen(const char *string_data) { const char *data_plaas = string_data; while (*data_plaas) data_plaas++; return data_plaas - string_data; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t item_COUNT) { const unsigned char *x_koördinaat = 첫째값, *Y_koördinaat = SECOND_VALUE; while (item_COUNT--) { if (*x_koördinaat != *Y_koördinaat) return (int)*x_koördinaat - *Y_koördinaat; x_koördinaat++; Y_koördinaat++; } return 0; }
void *memmove(void *bestemming_data, const void *string_data, size_t item_COUNT) { unsigned char *x_koördinaat = bestemming_data; const unsigned char *Y_koördinaat = string_data; if (x_koördinaat < Y_koördinaat) { for (size_t 순번 = 0; 순번 < item_COUNT; 순번++) x_koördinaat[순번] = Y_koördinaat[순번]; } else { while (item_COUNT) { item_COUNT--; x_koördinaat[item_COUNT] = Y_koördinaat[item_COUNT]; } } return bestemming_data; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t item_COUNT) { while (item_COUNT--) { unsigned char x_koördinaat = *첫째값++, Y_koördinaat = *SECOND_VALUE++; if (x_koördinaat != Y_koördinaat) return (int)x_koördinaat-Y_koördinaat; if (!x_koördinaat) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *string_data, char **beëindig_OFFSET, int muur_VALUE) {
    const char *BEGIN_OFFSET = string_data; unsigned long VALUE = 0; int enkodering_VALUE = 1, 하나라도 = 0;
    while (*string_data == ' ' || (*string_data >= 9 && *string_data <= 13)) string_data++;
    if (*string_data == '-' || *string_data == '+') { if (*string_data == '-') enkodering_VALUE = -1; string_data++; }
    if (muur_VALUE == 0) muur_VALUE = 10;
    while (*string_data >= '0' && *string_data <= '9' && *string_data - '0' < muur_VALUE) {
        unsigned syfer_VALUE = *string_data++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - syfer_VALUE) / (unsigned)muur_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * muur_VALUE + syfer_VALUE;
    }
    if (beëindig_OFFSET) *beëindig_OFFSET = (char *)(하나라도 ? string_data : BEGIN_OFFSET); return enkodering_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *string_data) { return (int)strtol(string_data, 0, 10); }
