#include "string.h"
size_t strlen(const char *rentetan_data) { const char *data_jawatan = rentetan_data; while (*data_jawatan) data_jawatan++; return data_jawatan - rentetan_data; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t item_COUNT) { const unsigned char *koordinat_x = 첫째값, *Y_koordinat = SECOND_VALUE; while (item_COUNT--) { if (*koordinat_x != *Y_koordinat) return (int)*koordinat_x - *Y_koordinat; koordinat_x++; Y_koordinat++; } return 0; }
void *memmove(void *destinasi_data, const void *rentetan_data, size_t item_COUNT) { unsigned char *koordinat_x = destinasi_data; const unsigned char *Y_koordinat = rentetan_data; if (koordinat_x < Y_koordinat) { for (size_t 순번 = 0; 순번 < item_COUNT; 순번++) koordinat_x[순번] = Y_koordinat[순번]; } else { while (item_COUNT) { item_COUNT--; koordinat_x[item_COUNT] = Y_koordinat[item_COUNT]; } } return destinasi_data; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t item_COUNT) { while (item_COUNT--) { unsigned char koordinat_x = *첫째값++, Y_koordinat = *SECOND_VALUE++; if (koordinat_x != Y_koordinat) return (int)koordinat_x-Y_koordinat; if (!koordinat_x) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *rentetan_data, char **tamat_Ofset, int latar_VALUE) {
    const char *Mula_Ofset = rentetan_data; unsigned long VALUE = 0; int pengekodan_VALUE = 1, 하나라도 = 0;
    while (*rentetan_data == ' ' || (*rentetan_data >= 9 && *rentetan_data <= 13)) rentetan_data++;
    if (*rentetan_data == '-' || *rentetan_data == '+') { if (*rentetan_data == '-') pengekodan_VALUE = -1; rentetan_data++; }
    if (latar_VALUE == 0) latar_VALUE = 10;
    while (*rentetan_data >= '0' && *rentetan_data <= '9' && *rentetan_data - '0' < latar_VALUE) {
        unsigned digit_VALUE = *rentetan_data++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - digit_VALUE) / (unsigned)latar_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * latar_VALUE + digit_VALUE;
    }
    if (tamat_Ofset) *tamat_Ofset = (char *)(하나라도 ? rentetan_data : Mula_Ofset); return pengekodan_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *rentetan_data) { return (int)strtol(rentetan_data, 0, 10); }
