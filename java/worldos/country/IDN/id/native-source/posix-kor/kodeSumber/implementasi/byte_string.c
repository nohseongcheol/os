#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *string_VALUE) { size_t panjang_VALUE = 0; while (string_VALUE[panjang_VALUE]) panjang_VALUE++; return panjang_VALUE; }
int strcmp(const char *depan_VALUE, const char *BACK_VALUE) {
    while (*depan_VALUE && *depan_VALUE == *BACK_VALUE) { depan_VALUE++; BACK_VALUE++; }
    return (unsigned char)*depan_VALUE - (unsigned char)*BACK_VALUE;
}
int memcmp(const void *depan_VALUE, const void *BACK_VALUE, size_t byte_COUNT) {
    const unsigned char *가 = depan_VALUE, *SECOND_operand = BACK_VALUE;
    for (size_t slot_entri = 0; slot_entri < byte_COUNT; slot_entri++) if (가[slot_entri] != SECOND_operand[slot_entri]) return 가[slot_entri] - SECOND_operand[slot_entri];
    return 0;
}
void *memcpy(void *tujuan_VALUE, const void *원본, size_t byte_COUNT) {
    unsigned char *가 = tujuan_VALUE; const unsigned char *SECOND_operand = 원본;
    for (size_t slot_entri = 0; slot_entri < byte_COUNT; slot_entri++) 가[slot_entri] = SECOND_operand[slot_entri];
    return tujuan_VALUE;
}
void *memset(void *tujuan_VALUE, int VALUE, size_t byte_COUNT) {
    unsigned char *data = tujuan_VALUE;
    for (size_t slot_entri = 0; slot_entri < byte_COUNT; slot_entri++) data[slot_entri] = VALUE;
    return tujuan_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *string_VALUE) {
    size_t panjang_VALUE = strlen(string_VALUE), posisi = 0;
    while (posisi < panjang_VALUE) { ssize_t hasil = write(1, string_VALUE + posisi, panjang_VALUE - posisi); if (hasil <= 0) return EOF; posisi += hasil; }
    return putchar('\n') == EOF ? EOF : 0;
}
