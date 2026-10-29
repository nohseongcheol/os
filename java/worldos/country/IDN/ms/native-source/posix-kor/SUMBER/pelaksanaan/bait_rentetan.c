#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *rentetan_VALUE) { size_t kepanjangan_VALUE = 0; while (rentetan_VALUE[kepanjangan_VALUE]) kepanjangan_VALUE++; return kepanjangan_VALUE; }
int strcmp(const char *hadapan_VALUE, const char *BACK_VALUE) {
    while (*hadapan_VALUE && *hadapan_VALUE == *BACK_VALUE) { hadapan_VALUE++; BACK_VALUE++; }
    return (unsigned char)*hadapan_VALUE - (unsigned char)*BACK_VALUE;
}
int memcmp(const void *hadapan_VALUE, const void *BACK_VALUE, size_t bait_COUNT) {
    const unsigned char *가 = hadapan_VALUE, *나 = BACK_VALUE;
    for (size_t 칸 = 0; 칸 < bait_COUNT; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *destinasi_VALUE, const void *원본, size_t bait_COUNT) {
    unsigned char *가 = destinasi_VALUE; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < bait_COUNT; 칸++) 가[칸] = 나[칸];
    return destinasi_VALUE;
}
void *memset(void *destinasi_VALUE, int VALUE, size_t bait_COUNT) {
    unsigned char *data = destinasi_VALUE;
    for (size_t 칸 = 0; 칸 < bait_COUNT; 칸++) data[칸] = VALUE;
    return destinasi_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *rentetan_VALUE) {
    size_t kepanjangan_VALUE = strlen(rentetan_VALUE), Kedudukan = 0;
    while (Kedudukan < kepanjangan_VALUE) { ssize_t ukuran = write(1, rentetan_VALUE + Kedudukan, kepanjangan_VALUE - Kedudukan); if (ukuran <= 0) return EOF; Kedudukan += ukuran; }
    return putchar('\n') == EOF ? EOF : 0;
}
