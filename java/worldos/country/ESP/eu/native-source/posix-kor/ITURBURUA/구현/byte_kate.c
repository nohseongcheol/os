#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *kate_balio) { size_t luzera_balio = 0; while (kate_balio[luzera_balio]) luzera_balio++; return luzera_balio; }
int strcmp(const char *aurrekoa_balio, const char *ATZERA_balio) {
    while (*aurrekoa_balio && *aurrekoa_balio == *ATZERA_balio) { aurrekoa_balio++; ATZERA_balio++; }
    return (unsigned char)*aurrekoa_balio - (unsigned char)*ATZERA_balio;
}
int memcmp(const void *aurrekoa_balio, const void *ATZERA_balio, size_t byte_ZENBATU) {
    const unsigned char *가 = aurrekoa_balio, *나 = ATZERA_balio;
    for (size_t 칸 = 0; 칸 < byte_ZENBATU; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *helburu_balio_a0fbc067, const void *원본, size_t byte_ZENBATU) {
    unsigned char *가 = helburu_balio_a0fbc067; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < byte_ZENBATU; 칸++) 가[칸] = 나[칸];
    return helburu_balio_a0fbc067;
}
void *memset(void *helburu_balio_a0fbc067, int balio, size_t byte_ZENBATU) {
    unsigned char *datuak = helburu_balio_a0fbc067;
    for (size_t 칸 = 0; 칸 < byte_ZENBATU; 칸++) datuak[칸] = balio;
    return helburu_balio_a0fbc067;
}
int putchar(int 문자) { unsigned char balio = 문자; return write(1, &balio, 1) == 1 ? balio : EOF; }
int puts(const char *kate_balio) {
    size_t luzera_balio = strlen(kate_balio), Posizioa = 0;
    while (Posizioa < luzera_balio) { ssize_t EMAITZA = write(1, kate_balio + Posizioa, luzera_balio - Posizioa); if (EMAITZA <= 0) return EOF; Posizioa += EMAITZA; }
    return putchar('\n') == EOF ? EOF : 0;
}
