#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *tekenreeks_WAARDE) { size_t tijdsduur_WAARDE = 0; while (tekenreeks_WAARDE[tijdsduur_WAARDE]) tijdsduur_WAARDE++; return tijdsduur_WAARDE; }
int strcmp(const char *voorkant_WAARDE, const char *BACK_WAARDE) {
    while (*voorkant_WAARDE && *voorkant_WAARDE == *BACK_WAARDE) { voorkant_WAARDE++; BACK_WAARDE++; }
    return (unsigned char)*voorkant_WAARDE - (unsigned char)*BACK_WAARDE;
}
int memcmp(const void *voorkant_WAARDE, const void *BACK_WAARDE, size_t byte_AANTAL) {
    const unsigned char *가 = voorkant_WAARDE, *SECONDE_operand = BACK_WAARDE;
    for (size_t sleuf_invoer = 0; sleuf_invoer < byte_AANTAL; sleuf_invoer++) if (가[sleuf_invoer] != SECONDE_operand[sleuf_invoer]) return 가[sleuf_invoer] - SECONDE_operand[sleuf_invoer];
    return 0;
}
void *memcpy(void *doel_WAARDE, const void *원본, size_t byte_AANTAL) {
    unsigned char *가 = doel_WAARDE; const unsigned char *SECONDE_operand = 원본;
    for (size_t sleuf_invoer = 0; sleuf_invoer < byte_AANTAL; sleuf_invoer++) 가[sleuf_invoer] = SECONDE_operand[sleuf_invoer];
    return doel_WAARDE;
}
void *memset(void *doel_WAARDE, int WAARDE, size_t byte_AANTAL) {
    unsigned char *gegevens = doel_WAARDE;
    for (size_t sleuf_invoer = 0; sleuf_invoer < byte_AANTAL; sleuf_invoer++) gegevens[sleuf_invoer] = WAARDE;
    return doel_WAARDE;
}
int putchar(int 문자) { unsigned char WAARDE = 문자; return write(1, &WAARDE, 1) == 1 ? WAARDE : EOF; }
int puts(const char *tekenreeks_WAARDE) {
    size_t tijdsduur_WAARDE = strlen(tekenreeks_WAARDE), positie = 0;
    while (positie < tijdsduur_WAARDE) { ssize_t resultaat = write(1, tekenreeks_WAARDE + positie, tijdsduur_WAARDE - positie); if (resultaat <= 0) return EOF; positie += resultaat; }
    return putchar('\n') == EOF ? EOF : 0;
}
