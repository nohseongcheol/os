#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ciąg_WARTOŚĆ) { size_t długość_WARTOŚĆ = 0; while (ciąg_WARTOŚĆ[długość_WARTOŚĆ]) długość_WARTOŚĆ++; return długość_WARTOŚĆ; }
int strcmp(const char *przód_WARTOŚĆ, const char *BACK_WARTOŚĆ) {
    while (*przód_WARTOŚĆ && *przód_WARTOŚĆ == *BACK_WARTOŚĆ) { przód_WARTOŚĆ++; BACK_WARTOŚĆ++; }
    return (unsigned char)*przód_WARTOŚĆ - (unsigned char)*BACK_WARTOŚĆ;
}
int memcmp(const void *przód_WARTOŚĆ, const void *BACK_WARTOŚĆ, size_t bajt_ILE_LICZB) {
    const unsigned char *가 = przód_WARTOŚĆ, *SEKUNDA_operand = BACK_WARTOŚĆ;
    for (size_t gniazdo_wpis = 0; gniazdo_wpis < bajt_ILE_LICZB; gniazdo_wpis++) if (가[gniazdo_wpis] != SEKUNDA_operand[gniazdo_wpis]) return 가[gniazdo_wpis] - SEKUNDA_operand[gniazdo_wpis];
    return 0;
}
void *memcpy(void *cel_WARTOŚĆ, const void *원본, size_t bajt_ILE_LICZB) {
    unsigned char *가 = cel_WARTOŚĆ; const unsigned char *SEKUNDA_operand = 원본;
    for (size_t gniazdo_wpis = 0; gniazdo_wpis < bajt_ILE_LICZB; gniazdo_wpis++) 가[gniazdo_wpis] = SEKUNDA_operand[gniazdo_wpis];
    return cel_WARTOŚĆ;
}
void *memset(void *cel_WARTOŚĆ, int WARTOŚĆ, size_t bajt_ILE_LICZB) {
    unsigned char *dane = cel_WARTOŚĆ;
    for (size_t gniazdo_wpis = 0; gniazdo_wpis < bajt_ILE_LICZB; gniazdo_wpis++) dane[gniazdo_wpis] = WARTOŚĆ;
    return cel_WARTOŚĆ;
}
int putchar(int 문자) { unsigned char WARTOŚĆ = 문자; return write(1, &WARTOŚĆ, 1) == 1 ? WARTOŚĆ : EOF; }
int puts(const char *ciąg_WARTOŚĆ) {
    size_t długość_WARTOŚĆ = strlen(ciąg_WARTOŚĆ), pozycja = 0;
    while (pozycja < długość_WARTOŚĆ) { ssize_t WYNIK = write(1, ciąg_WARTOŚĆ + pozycja, długość_WARTOŚĆ - pozycja); if (WYNIK <= 0) return EOF; pozycja += WYNIK; }
    return putchar('\n') == EOF ? EOF : 0;
}
