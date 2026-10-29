#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *string_VALUE) { size_t dužina_VALUE = 0; while (string_VALUE[dužina_VALUE]) dužina_VALUE++; return dužina_VALUE; }
int strcmp(const char *앞, const char *ZAD_VALUE) {
    while (*앞 && *앞 == *ZAD_VALUE) { 앞++; ZAD_VALUE++; }
    return (unsigned char)*앞 - (unsigned char)*ZAD_VALUE;
}
int memcmp(const void *앞, const void *ZAD_VALUE, size_t bajt_COUNT) {
    const unsigned char *가 = 앞, *SECOND_operand = ZAD_VALUE;
    for (size_t prostor_za_unos_unos = 0; prostor_za_unos_unos < bajt_COUNT; prostor_za_unos_unos++) if (가[prostor_za_unos_unos] != SECOND_operand[prostor_za_unos_unos]) return 가[prostor_za_unos_unos] - SECOND_operand[prostor_za_unos_unos];
    return 0;
}
void *memcpy(void *odredište_VALUE, const void *원본, size_t bajt_COUNT) {
    unsigned char *가 = odredište_VALUE; const unsigned char *SECOND_operand = 원본;
    for (size_t prostor_za_unos_unos = 0; prostor_za_unos_unos < bajt_COUNT; prostor_za_unos_unos++) 가[prostor_za_unos_unos] = SECOND_operand[prostor_za_unos_unos];
    return odredište_VALUE;
}
void *memset(void *odredište_VALUE, int VALUE, size_t bajt_COUNT) {
    unsigned char *podaci = odredište_VALUE;
    for (size_t prostor_za_unos_unos = 0; prostor_za_unos_unos < bajt_COUNT; prostor_za_unos_unos++) podaci[prostor_za_unos_unos] = VALUE;
    return odredište_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *string_VALUE) {
    size_t dužina_VALUE = strlen(string_VALUE), Pozicija = 0;
    while (Pozicija < dužina_VALUE) { ssize_t mjera = write(1, string_VALUE + Pozicija, dužina_VALUE - Pozicija); if (mjera <= 0) return EOF; Pozicija += mjera; }
    return putchar('\n') == EOF ? EOF : 0;
}
