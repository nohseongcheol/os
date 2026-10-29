#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *sətir_VALUE) { size_t uzunluq_VALUE = 0; while (sətir_VALUE[uzunluq_VALUE]) uzunluq_VALUE++; return uzunluq_VALUE; }
int strcmp(const char *ön_VALUE, const char *GERİ_VALUE) {
    while (*ön_VALUE && *ön_VALUE == *GERİ_VALUE) { ön_VALUE++; GERİ_VALUE++; }
    return (unsigned char)*ön_VALUE - (unsigned char)*GERİ_VALUE;
}
int memcmp(const void *ön_VALUE, const void *GERİ_VALUE, size_t bayt_COUNT) {
    const unsigned char *가 = ön_VALUE, *나 = GERİ_VALUE;
    for (size_t slot_daxiletmə = 0; slot_daxiletmə < bayt_COUNT; slot_daxiletmə++) if (가[slot_daxiletmə] != 나[slot_daxiletmə]) return 가[slot_daxiletmə] - 나[slot_daxiletmə];
    return 0;
}
void *memcpy(void *təyinat_VALUE_a0fbc067, const void *원본, size_t bayt_COUNT) {
    unsigned char *가 = təyinat_VALUE_a0fbc067; const unsigned char *나 = 원본;
    for (size_t slot_daxiletmə = 0; slot_daxiletmə < bayt_COUNT; slot_daxiletmə++) 가[slot_daxiletmə] = 나[slot_daxiletmə];
    return təyinat_VALUE_a0fbc067;
}
void *memset(void *təyinat_VALUE_a0fbc067, int VALUE, size_t bayt_COUNT) {
    unsigned char *verilənlər = təyinat_VALUE_a0fbc067;
    for (size_t slot_daxiletmə = 0; slot_daxiletmə < bayt_COUNT; slot_daxiletmə++) verilənlər[slot_daxiletmə] = VALUE;
    return təyinat_VALUE_a0fbc067;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *sətir_VALUE) {
    size_t uzunluq_VALUE = strlen(sətir_VALUE), yerinə_qoymaq = 0;
    while (yerinə_qoymaq < uzunluq_VALUE) { ssize_t ölçü = write(1, sətir_VALUE + yerinə_qoymaq, uzunluq_VALUE - yerinə_qoymaq); if (ölçü <= 0) return EOF; yerinə_qoymaq += ölçü; }
    return putchar('\n') == EOF ? EOF : 0;
}
