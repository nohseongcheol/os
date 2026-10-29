#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *řetězec_HODNOTA) { size_t délka_HODNOTA = 0; while (řetězec_HODNOTA[délka_HODNOTA]) délka_HODNOTA++; return délka_HODNOTA; }
int strcmp(const char *přední_fotoaparát_HODNOTA, const char *BACK_HODNOTA) {
    while (*přední_fotoaparát_HODNOTA && *přední_fotoaparát_HODNOTA == *BACK_HODNOTA) { přední_fotoaparát_HODNOTA++; BACK_HODNOTA++; }
    return (unsigned char)*přední_fotoaparát_HODNOTA - (unsigned char)*BACK_HODNOTA;
}
int memcmp(const void *přední_fotoaparát_HODNOTA, const void *BACK_HODNOTA, size_t bajt_POČET) {
    const unsigned char *가 = přední_fotoaparát_HODNOTA, *SEKUNDA_operand = BACK_HODNOTA;
    for (size_t přihrádka_položka = 0; přihrádka_položka < bajt_POČET; přihrádka_položka++) if (가[přihrádka_položka] != SEKUNDA_operand[přihrádka_položka]) return 가[přihrádka_položka] - SEKUNDA_operand[přihrádka_položka];
    return 0;
}
void *memcpy(void *cíl_HODNOTA, const void *원본, size_t bajt_POČET) {
    unsigned char *가 = cíl_HODNOTA; const unsigned char *SEKUNDA_operand = 원본;
    for (size_t přihrádka_položka = 0; přihrádka_položka < bajt_POČET; přihrádka_položka++) 가[přihrádka_položka] = SEKUNDA_operand[přihrádka_položka];
    return cíl_HODNOTA;
}
void *memset(void *cíl_HODNOTA, int HODNOTA, size_t bajt_POČET) {
    unsigned char *data = cíl_HODNOTA;
    for (size_t přihrádka_položka = 0; přihrádka_položka < bajt_POČET; přihrádka_položka++) data[přihrádka_položka] = HODNOTA;
    return cíl_HODNOTA;
}
int putchar(int 문자) { unsigned char HODNOTA = 문자; return write(1, &HODNOTA, 1) == 1 ? HODNOTA : EOF; }
int puts(const char *řetězec_HODNOTA) {
    size_t délka_HODNOTA = strlen(řetězec_HODNOTA), pozice = 0;
    while (pozice < délka_HODNOTA) { ssize_t VÝSLEDEK = write(1, řetězec_HODNOTA + pozice, délka_HODNOTA - pozice); if (VÝSLEDEK <= 0) return EOF; pozice += VÝSLEDEK; }
    return putchar('\n') == EOF ? EOF : 0;
}
