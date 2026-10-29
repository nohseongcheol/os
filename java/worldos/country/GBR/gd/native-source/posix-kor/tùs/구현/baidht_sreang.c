#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *sreang_VALUE) { size_t faid_VALUE = 0; while (sreang_VALUE[faid_VALUE]) faid_VALUE++; return faid_VALUE; }
int strcmp(const char *앞, const char *Air_ais_VALUE) {
    while (*앞 && *앞 == *Air_ais_VALUE) { 앞++; Air_ais_VALUE++; }
    return (unsigned char)*앞 - (unsigned char)*Air_ais_VALUE;
}
int memcmp(const void *앞, const void *Air_ais_VALUE, size_t baidht_COUNT) {
    const unsigned char *가 = 앞, *나 = Air_ais_VALUE;
    for (size_t slot_cur_a_steach = 0; slot_cur_a_steach < baidht_COUNT; slot_cur_a_steach++) if (가[slot_cur_a_steach] != 나[slot_cur_a_steach]) return 가[slot_cur_a_steach] - 나[slot_cur_a_steach];
    return 0;
}
void *memcpy(void *ceann_uidhe_VALUE, const void *원본, size_t baidht_COUNT) {
    unsigned char *가 = ceann_uidhe_VALUE; const unsigned char *나 = 원본;
    for (size_t slot_cur_a_steach = 0; slot_cur_a_steach < baidht_COUNT; slot_cur_a_steach++) 가[slot_cur_a_steach] = 나[slot_cur_a_steach];
    return ceann_uidhe_VALUE;
}
void *memset(void *ceann_uidhe_VALUE, int VALUE, size_t baidht_COUNT) {
    unsigned char *dàta = ceann_uidhe_VALUE;
    for (size_t slot_cur_a_steach = 0; slot_cur_a_steach < baidht_COUNT; slot_cur_a_steach++) dàta[slot_cur_a_steach] = VALUE;
    return ceann_uidhe_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *sreang_VALUE) {
    size_t faid_VALUE = strlen(sreang_VALUE), suidhich = 0;
    while (suidhich < faid_VALUE) { ssize_t tomhas = write(1, sreang_VALUE + suidhich, faid_VALUE - suidhich); if (tomhas <= 0) return EOF; suidhich += tomhas; }
    return putchar('\n') == EOF ? EOF : 0;
}
