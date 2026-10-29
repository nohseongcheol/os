#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *testun_VALUE) { size_t hyd_VALUE = 0; while (testun_VALUE[hyd_VALUE]) hyd_VALUE++; return hyd_VALUE; }
int strcmp(const char *앞, const char *BACK_VALUE) {
    while (*앞 && *앞 == *BACK_VALUE) { 앞++; BACK_VALUE++; }
    return (unsigned char)*앞 - (unsigned char)*BACK_VALUE;
}
int memcmp(const void *앞, const void *BACK_VALUE, size_t beit_COUNT) {
    const unsigned char *가 = 앞, *나 = BACK_VALUE;
    for (size_t slot_cofnod = 0; slot_cofnod < beit_COUNT; slot_cofnod++) if (가[slot_cofnod] != 나[slot_cofnod]) return 가[slot_cofnod] - 나[slot_cofnod];
    return 0;
}
void *memcpy(void *cyrchfan_VALUE, const void *원본, size_t beit_COUNT) {
    unsigned char *가 = cyrchfan_VALUE; const unsigned char *나 = 원본;
    for (size_t slot_cofnod = 0; slot_cofnod < beit_COUNT; slot_cofnod++) 가[slot_cofnod] = 나[slot_cofnod];
    return cyrchfan_VALUE;
}
void *memset(void *cyrchfan_VALUE, int VALUE, size_t beit_COUNT) {
    unsigned char *data = cyrchfan_VALUE;
    for (size_t slot_cofnod = 0; slot_cofnod < beit_COUNT; slot_cofnod++) data[slot_cofnod] = VALUE;
    return cyrchfan_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *testun_VALUE) {
    size_t hyd_VALUE = strlen(testun_VALUE), safle = 0;
    while (safle < hyd_VALUE) { ssize_t mesur = write(1, testun_VALUE + safle, hyd_VALUE - safle); if (mesur <= 0) return EOF; safle += mesur; }
    return putchar('\n') == EOF ? EOF : 0;
}
