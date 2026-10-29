#include "string.h"
size_t strlen(const char *datosCadena) { const char *posiciónDatos = datosCadena; while (*posiciónDatos) posiciónDatos++; return posiciónDatos - datosCadena; }
int memcmp(const void *valorPrimero, const void *valorSegundo, size_t númeroElementosElementoLista) { const unsigned char *coordenadaCoordenadaHorizontal = valorPrimero, *coordenadaCoordenadaVertical = valorSegundo; while (númeroElementosElementoLista--) { if (*coordenadaCoordenadaHorizontal != *coordenadaCoordenadaVertical) return (int)*coordenadaCoordenadaHorizontal - *coordenadaCoordenadaVertical; coordenadaCoordenadaHorizontal++; coordenadaCoordenadaVertical++; } return 0; }
void *memmove(void *datosDestino, const void *datosCadena, size_t númeroElementosElementoLista) { unsigned char *coordenadaCoordenadaHorizontal = datosDestino; const unsigned char *coordenadaCoordenadaVertical = datosCadena; if (coordenadaCoordenadaHorizontal < coordenadaCoordenadaVertical) { for (size_t índiceOrdinal = 0; índiceOrdinal < númeroElementosElementoLista; índiceOrdinal++) coordenadaCoordenadaHorizontal[índiceOrdinal] = coordenadaCoordenadaVertical[índiceOrdinal]; } else { while (númeroElementosElementoLista) { númeroElementosElementoLista--; coordenadaCoordenadaHorizontal[númeroElementosElementoLista] = coordenadaCoordenadaVertical[númeroElementosElementoLista]; } } return datosDestino; }
int strncmp(const char *valorPrimero, const char *valorSegundo, size_t númeroElementosElementoLista) { while (númeroElementosElementoLista--) { unsigned char coordenadaCoordenadaHorizontal = *valorPrimero++, coordenadaCoordenadaVertical = *valorSegundo++; if (coordenadaCoordenadaHorizontal != coordenadaCoordenadaVertical) return (int)coordenadaCoordenadaHorizontal-coordenadaCoordenadaVertical; if (!coordenadaCoordenadaHorizontal) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *datosCadena, char **desfaseFin, int valorFondo) {
    const char *iniciarDesfase = datosCadena; unsigned long valor = 0; int valorCodificaciónEstado = 1, valorCualquiera = 0;
    while (*datosCadena == ' ' || (*datosCadena >= 9 && *datosCadena <= 13)) datosCadena++;
    if (*datosCadena == '-' || *datosCadena == '+') { if (*datosCadena == '-') valorCodificaciónEstado = -1; datosCadena++; }
    if (valorFondo == 0) valorFondo = 10;
    while (*datosCadena >= '0' && *datosCadena <= '9' && *datosCadena - '0' < valorFondo) {
        unsigned valorDígito = *datosCadena++ - '0'; valorCualquiera = 1;
        if (valor > (0x7ffffffffffffffful - valorDígito) / (unsigned)valorFondo) valor = 0x7ffffffffffffffful;
        else valor = valor * valorFondo + valorDígito;
    }
    if (desfaseFin) *desfaseFin = (char *)(valorCualquiera ? datosCadena : iniciarDesfase); return valorCodificaciónEstado > 0 ? (long)valor : -(long)valor;
}
int atoi(const char *datosCadena) { return (int)strtol(datosCadena, 0, 10); }
