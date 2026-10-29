#include "string.h"
size_t strlen(const char *cadea_datos) { const char *datos_cargo = cadea_datos; while (*datos_cargo) datos_cargo++; return datos_cargo - cadea_datos; }
int memcmp(const void *첫째값, const void *SEGUNDO_VALOR, size_t elemento_CONTAR) { const unsigned char *X_coordenada = 첫째값, *Y_coordenada = SEGUNDO_VALOR; while (elemento_CONTAR--) { if (*X_coordenada != *Y_coordenada) return (int)*X_coordenada - *Y_coordenada; X_coordenada++; Y_coordenada++; } return 0; }
void *memmove(void *destino_datos, const void *cadea_datos, size_t elemento_CONTAR) { unsigned char *X_coordenada = destino_datos; const unsigned char *Y_coordenada = cadea_datos; if (X_coordenada < Y_coordenada) { for (size_t 순번 = 0; 순번 < elemento_CONTAR; 순번++) X_coordenada[순번] = Y_coordenada[순번]; } else { while (elemento_CONTAR) { elemento_CONTAR--; X_coordenada[elemento_CONTAR] = Y_coordenada[elemento_CONTAR]; } } return destino_datos; }
int strncmp(const char *첫째값, const char *SEGUNDO_VALOR, size_t elemento_CONTAR) { while (elemento_CONTAR--) { unsigned char X_coordenada = *첫째값++, Y_coordenada = *SEGUNDO_VALOR++; if (X_coordenada != Y_coordenada) return (int)X_coordenada-Y_coordenada; if (!X_coordenada) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *cadea_datos, char **finalizar_DESPRAZAMENTO, int Fondo_VALOR) {
    const char *START_DESPRAZAMENTO = cadea_datos; unsigned long VALOR = 0; int codificación_VALOR = 1, 하나라도 = 0;
    while (*cadea_datos == ' ' || (*cadea_datos >= 9 && *cadea_datos <= 13)) cadea_datos++;
    if (*cadea_datos == '-' || *cadea_datos == '+') { if (*cadea_datos == '-') codificación_VALOR = -1; cadea_datos++; }
    if (Fondo_VALOR == 0) Fondo_VALOR = 10;
    while (*cadea_datos >= '0' && *cadea_datos <= '9' && *cadea_datos - '0' < Fondo_VALOR) {
        unsigned díxito_VALOR = *cadea_datos++ - '0'; 하나라도 = 1;
        if (VALOR > (0x7ffffffffffffffful - díxito_VALOR) / (unsigned)Fondo_VALOR) VALOR = 0x7ffffffffffffffful;
        else VALOR = VALOR * Fondo_VALOR + díxito_VALOR;
    }
    if (finalizar_DESPRAZAMENTO) *finalizar_DESPRAZAMENTO = (char *)(하나라도 ? cadea_datos : START_DESPRAZAMENTO); return codificación_VALOR > 0 ? (long)VALOR : -(long)VALOR;
}
int atoi(const char *cadea_datos) { return (int)strtol(cadea_datos, 0, 10); }
