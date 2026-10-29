#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *жол_мән_6ca8363c) { size_t ұзындық_мән = 0; while (жол_мән_6ca8363c[ұзындық_мән]) ұзындық_мән++; return ұзындық_мән; }
int strcmp(const char *алдыңғы_камера_мән, const char *АРТҚА_мән) {
    while (*алдыңғы_камера_мән && *алдыңғы_камера_мән == *АРТҚА_мән) { алдыңғы_камера_мән++; АРТҚА_мән++; }
    return (unsigned char)*алдыңғы_камера_мән - (unsigned char)*АРТҚА_мән;
}
int memcmp(const void *алдыңғы_камера_мән, const void *АРТҚА_мән, size_t 바이트수) {
    const unsigned char *가 = алдыңғы_камера_мән, *나 = АРТҚА_мән;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *тағайындау_мән, const void *원본, size_t 바이트수) {
    unsigned char *가 = тағайындау_мән; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 가[칸] = 나[칸];
    return тағайындау_мән;
}
void *memset(void *тағайындау_мән, int мән, size_t 바이트수) {
    unsigned char *деректер = тағайындау_мән;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) деректер[칸] = мән;
    return тағайындау_мән;
}
int putchar(int 문자) { unsigned char мән = 문자; return write(1, &мән, 1) == 1 ? мән : EOF; }
int puts(const char *жол_мән_6ca8363c) {
    size_t ұзындық_мән = strlen(жол_мән_6ca8363c), Орны = 0;
    while (Орны < ұзындық_мән) { ssize_t НӘТИЖЕ = write(1, жол_мән_6ca8363c + Орны, ұзындық_мән - Орны); if (НӘТИЖЕ <= 0) return EOF; Орны += НӘТИЖЕ; }
    return putchar('\n') == EOF ? EOF : 0;
}
