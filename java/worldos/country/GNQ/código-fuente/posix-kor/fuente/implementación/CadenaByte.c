#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *Cadena) { size_t longitud = 0; while (Cadena[longitud]) longitud++; return longitud; }
int strcmp(const char *valorLadoDelantero, const char *valorLadoPosterior) {
    while (*valorLadoDelantero && *valorLadoDelantero == *valorLadoPosterior) { valorLadoDelantero++; valorLadoPosterior++; }
    return (unsigned char)*valorLadoDelantero - (unsigned char)*valorLadoPosterior;
}
int memcmp(const void *valorLadoDelantero, const void *valorLadoPosterior, size_t númeroElementosByte) {
    const unsigned char *operandoPrimero = valorLadoDelantero, *operandoSegundo = valorLadoPosterior;
    for (size_t entradaElementoRanura = 0; entradaElementoRanura < númeroElementosByte; entradaElementoRanura++) if (operandoPrimero[entradaElementoRanura] != operandoSegundo[entradaElementoRanura]) return operandoPrimero[entradaElementoRanura] - operandoSegundo[entradaElementoRanura];
    return 0;
}
void *memcpy(void *valorDestino, const void *original, size_t númeroElementosByte) {
    unsigned char *operandoPrimero = valorDestino; const unsigned char *operandoSegundo = original;
    for (size_t entradaElementoRanura = 0; entradaElementoRanura < númeroElementosByte; entradaElementoRanura++) operandoPrimero[entradaElementoRanura] = operandoSegundo[entradaElementoRanura];
    return valorDestino;
}
void *memset(void *valorDestino, int valor, size_t númeroElementosByte) {
    unsigned char *Datos = valorDestino;
    for (size_t entradaElementoRanura = 0; entradaElementoRanura < númeroElementosByte; entradaElementoRanura++) Datos[entradaElementoRanura] = valor;
    return valorDestino;
}
int putchar(int Caracteres) { unsigned char valor = Caracteres; return write(1, &valor, 1) == 1 ? valor : EOF; }
int puts(const char *Cadena) {
    size_t longitud = strlen(Cadena), posición = 0;
    while (posición < longitud) { ssize_t resultado = write(1, Cadena + posición, longitud - posición); if (resultado <= 0) return EOF; posición += resultado; }
    return putchar('\n') == EOF ? EOF : 0;
}
