#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *cadena_VALOR) { size_t durada_VALOR = 0; while (cadena_VALOR[durada_VALOR]) durada_VALOR++; return durada_VALOR; }
int strcmp(const char *frontal_VALOR, const char *ENRERE_VALOR) {
    while (*frontal_VALOR && *frontal_VALOR == *ENRERE_VALOR) { frontal_VALOR++; ENRERE_VALOR++; }
    return (unsigned char)*frontal_VALOR - (unsigned char)*ENRERE_VALOR;
}
int memcmp(const void *frontal_VALOR, const void *ENRERE_VALOR, size_t byte_COMPT) {
    const unsigned char *가 = frontal_VALOR, *나 = ENRERE_VALOR;
    for (size_t 칸 = 0; 칸 < byte_COMPT; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *destinació_VALOR, const void *원본, size_t byte_COMPT) {
    unsigned char *가 = destinació_VALOR; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < byte_COMPT; 칸++) 가[칸] = 나[칸];
    return destinació_VALOR;
}
void *memset(void *destinació_VALOR, int VALOR, size_t byte_COMPT) {
    unsigned char *dades = destinació_VALOR;
    for (size_t 칸 = 0; 칸 < byte_COMPT; 칸++) dades[칸] = VALOR;
    return destinació_VALOR;
}
int putchar(int 문자) { unsigned char VALOR = 문자; return write(1, &VALOR, 1) == 1 ? VALOR : EOF; }
int puts(const char *cadena_VALOR) {
    size_t durada_VALOR = strlen(cadena_VALOR), Posició = 0;
    while (Posició < durada_VALOR) { ssize_t RESULTAT = write(1, cadena_VALOR + Posició, durada_VALOR - Posició); if (RESULTAT <= 0) return EOF; Posició += RESULTAT; }
    return putchar('\n') == EOF ? EOF : 0;
}
