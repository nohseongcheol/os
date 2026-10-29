#include "string.h"
size_t strlen(const char *cadena_dades) { const char *dades_càrrec = cadena_dades; while (*dades_càrrec) dades_càrrec++; return dades_càrrec - cadena_dades; }
int memcmp(const void *첫째값, const void *SEGON_VALOR, size_t element_COMPT) { const unsigned char *X_coordenada = 첫째값, *Y_coordenada = SEGON_VALOR; while (element_COMPT--) { if (*X_coordenada != *Y_coordenada) return (int)*X_coordenada - *Y_coordenada; X_coordenada++; Y_coordenada++; } return 0; }
void *memmove(void *destinació_dades, const void *cadena_dades, size_t element_COMPT) { unsigned char *X_coordenada = destinació_dades; const unsigned char *Y_coordenada = cadena_dades; if (X_coordenada < Y_coordenada) { for (size_t 순번 = 0; 순번 < element_COMPT; 순번++) X_coordenada[순번] = Y_coordenada[순번]; } else { while (element_COMPT) { element_COMPT--; X_coordenada[element_COMPT] = Y_coordenada[element_COMPT]; } } return destinació_dades; }
int strncmp(const char *첫째값, const char *SEGON_VALOR, size_t element_COMPT) { while (element_COMPT--) { unsigned char X_coordenada = *첫째값++, Y_coordenada = *SEGON_VALOR++; if (X_coordenada != Y_coordenada) return (int)X_coordenada-Y_coordenada; if (!X_coordenada) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *cadena_dades, char **finalitzar_DESPLAÇAMENT, int Fons_VALOR) {
    const char *Inici_DESPLAÇAMENT = cadena_dades; unsigned long VALOR = 0; int codificació_VALOR = 1, 하나라도 = 0;
    while (*cadena_dades == ' ' || (*cadena_dades >= 9 && *cadena_dades <= 13)) cadena_dades++;
    if (*cadena_dades == '-' || *cadena_dades == '+') { if (*cadena_dades == '-') codificació_VALOR = -1; cadena_dades++; }
    if (Fons_VALOR == 0) Fons_VALOR = 10;
    while (*cadena_dades >= '0' && *cadena_dades <= '9' && *cadena_dades - '0' < Fons_VALOR) {
        unsigned dígit_VALOR = *cadena_dades++ - '0'; 하나라도 = 1;
        if (VALOR > (0x7ffffffffffffffful - dígit_VALOR) / (unsigned)Fons_VALOR) VALOR = 0x7ffffffffffffffful;
        else VALOR = VALOR * Fons_VALOR + dígit_VALOR;
    }
    if (finalitzar_DESPLAÇAMENT) *finalitzar_DESPLAÇAMENT = (char *)(하나라도 ? cadena_dades : Inici_DESPLAÇAMENT); return codificació_VALOR > 0 ? (long)VALOR : -(long)VALOR;
}
int atoi(const char *cadena_dades) { return (int)strtol(cadena_dades, 0, 10); }
