#include "string.h"
size_t strlen(const char *strengur_gögn) { const char *gögn_staða = strengur_gögn; while (*gögn_staða) gögn_staða++; return gögn_staða - strengur_gögn; }
int memcmp(const void *첫째값, const void *SECOND_VALUE, size_t vara_COUNT) { const unsigned char *x_hnit = 첫째값, *Y_hnit = SECOND_VALUE; while (vara_COUNT--) { if (*x_hnit != *Y_hnit) return (int)*x_hnit - *Y_hnit; x_hnit++; Y_hnit++; } return 0; }
void *memmove(void *endastaður_gögn, const void *strengur_gögn, size_t vara_COUNT) { unsigned char *x_hnit = endastaður_gögn; const unsigned char *Y_hnit = strengur_gögn; if (x_hnit < Y_hnit) { for (size_t 순번 = 0; 순번 < vara_COUNT; 순번++) x_hnit[순번] = Y_hnit[순번]; } else { while (vara_COUNT) { vara_COUNT--; x_hnit[vara_COUNT] = Y_hnit[vara_COUNT]; } } return endastaður_gögn; }
int strncmp(const char *첫째값, const char *SECOND_VALUE, size_t vara_COUNT) { while (vara_COUNT--) { unsigned char x_hnit = *첫째값++, Y_hnit = *SECOND_VALUE++; if (x_hnit != Y_hnit) return (int)x_hnit-Y_hnit; if (!x_hnit) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *strengur_gögn, char **ljúka_OFFSET, int veggfóður_VALUE) {
    const char *Opna_OFFSET = strengur_gögn; unsigned long VALUE = 0; int kóðun_VALUE = 1, 하나라도 = 0;
    while (*strengur_gögn == ' ' || (*strengur_gögn >= 9 && *strengur_gögn <= 13)) strengur_gögn++;
    if (*strengur_gögn == '-' || *strengur_gögn == '+') { if (*strengur_gögn == '-') kóðun_VALUE = -1; strengur_gögn++; }
    if (veggfóður_VALUE == 0) veggfóður_VALUE = 10;
    while (*strengur_gögn >= '0' && *strengur_gögn <= '9' && *strengur_gögn - '0' < veggfóður_VALUE) {
        unsigned tölustafur_VALUE = *strengur_gögn++ - '0'; 하나라도 = 1;
        if (VALUE > (0x7ffffffffffffffful - tölustafur_VALUE) / (unsigned)veggfóður_VALUE) VALUE = 0x7ffffffffffffffful;
        else VALUE = VALUE * veggfóður_VALUE + tölustafur_VALUE;
    }
    if (ljúka_OFFSET) *ljúka_OFFSET = (char *)(하나라도 ? strengur_gögn : Opna_OFFSET); return kóðun_VALUE > 0 ? (long)VALUE : -(long)VALUE;
}
int atoi(const char *strengur_gögn) { return (int)strtol(strengur_gögn, 0, 10); }
