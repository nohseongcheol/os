#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *cadea_VALOR) { size_t duración_VALOR = 0; while (cadea_VALOR[duración_VALOR]) duración_VALOR++; return duración_VALOR; }
int strcmp(const char *frontal_VALOR, const char *ATRÁS_VALOR) {
    while (*frontal_VALOR && *frontal_VALOR == *ATRÁS_VALOR) { frontal_VALOR++; ATRÁS_VALOR++; }
    return (unsigned char)*frontal_VALOR - (unsigned char)*ATRÁS_VALOR;
}
int memcmp(const void *frontal_VALOR, const void *ATRÁS_VALOR, size_t byte_CONTAR) {
    const unsigned char *가 = frontal_VALOR, *나 = ATRÁS_VALOR;
    for (size_t 칸 = 0; 칸 < byte_CONTAR; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *destino_VALOR, const void *원본, size_t byte_CONTAR) {
    unsigned char *가 = destino_VALOR; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < byte_CONTAR; 칸++) 가[칸] = 나[칸];
    return destino_VALOR;
}
void *memset(void *destino_VALOR, int VALOR, size_t byte_CONTAR) {
    unsigned char *datos = destino_VALOR;
    for (size_t 칸 = 0; 칸 < byte_CONTAR; 칸++) datos[칸] = VALOR;
    return destino_VALOR;
}
int putchar(int 문자) { unsigned char VALOR = 문자; return write(1, &VALOR, 1) == 1 ? VALOR : EOF; }
int puts(const char *cadea_VALOR) {
    size_t duración_VALOR = strlen(cadea_VALOR), Posición = 0;
    while (Posición < duración_VALOR) { ssize_t RESULTANTE = write(1, cadea_VALOR + Posición, duración_VALOR - Posición); if (RESULTANTE <= 0) return EOF; Posición += RESULTANTE; }
    return putchar('\n') == EOF ? EOF : 0;
}
