#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *stringa_VALORE) { size_t durata_VALORE = 0; while (stringa_VALORE[durata_VALORE]) durata_VALORE++; return durata_VALORE; }
int strcmp(const char *frontale_VALORE, const char *BACK_VALORE) {
    while (*frontale_VALORE && *frontale_VALORE == *BACK_VALORE) { frontale_VALORE++; BACK_VALORE++; }
    return (unsigned char)*frontale_VALORE - (unsigned char)*BACK_VALORE;
}
int memcmp(const void *frontale_VALORE, const void *BACK_VALORE, size_t byte_CONTA_NUMERI) {
    const unsigned char *가 = frontale_VALORE, *SECONDO_operando = BACK_VALORE;
    for (size_t slot_voce = 0; slot_voce < byte_CONTA_NUMERI; slot_voce++) if (가[slot_voce] != SECONDO_operando[slot_voce]) return 가[slot_voce] - SECONDO_operando[slot_voce];
    return 0;
}
void *memcpy(void *meta_VALORE, const void *원본, size_t byte_CONTA_NUMERI) {
    unsigned char *가 = meta_VALORE; const unsigned char *SECONDO_operando = 원본;
    for (size_t slot_voce = 0; slot_voce < byte_CONTA_NUMERI; slot_voce++) 가[slot_voce] = SECONDO_operando[slot_voce];
    return meta_VALORE;
}
void *memset(void *meta_VALORE, int VALORE, size_t byte_CONTA_NUMERI) {
    unsigned char *dati = meta_VALORE;
    for (size_t slot_voce = 0; slot_voce < byte_CONTA_NUMERI; slot_voce++) dati[slot_voce] = VALORE;
    return meta_VALORE;
}
int putchar(int 문자) { unsigned char VALORE = 문자; return write(1, &VALORE, 1) == 1 ? VALORE : EOF; }
int puts(const char *stringa_VALORE) {
    size_t durata_VALORE = strlen(stringa_VALORE), posizione = 0;
    while (posizione < durata_VALORE) { ssize_t risultato = write(1, stringa_VALORE + posizione, durata_VALORE - posizione); if (risultato <= 0) return EOF; posizione += risultato; }
    return putchar('\n') == EOF ? EOF : 0;
}
