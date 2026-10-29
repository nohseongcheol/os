#include "string.h"
size_t strlen(const char *cadeia_dados) { const char *dados_cargo = cadeia_dados; while (*dados_cargo) dados_cargo++; return dados_cargo - cadeia_dados; }
int memcmp(const void *첫째값, const void *SEGUNDO_VALOR, size_t item_CONT_NÚM) { const unsigned char *coordenada_X = 첫째값, *Y_coordenada = SEGUNDO_VALOR; while (item_CONT_NÚM--) { if (*coordenada_X != *Y_coordenada) return (int)*coordenada_X - *Y_coordenada; coordenada_X++; Y_coordenada++; } return 0; }
void *memmove(void *destino_dados, const void *cadeia_dados, size_t item_CONT_NÚM) { unsigned char *coordenada_X = destino_dados; const unsigned char *Y_coordenada = cadeia_dados; if (coordenada_X < Y_coordenada) { for (size_t 순번 = 0; 순번 < item_CONT_NÚM; 순번++) coordenada_X[순번] = Y_coordenada[순번]; } else { while (item_CONT_NÚM) { item_CONT_NÚM--; coordenada_X[item_CONT_NÚM] = Y_coordenada[item_CONT_NÚM]; } } return destino_dados; }
int strncmp(const char *첫째값, const char *SEGUNDO_VALOR, size_t item_CONT_NÚM) { while (item_CONT_NÚM--) { unsigned char coordenada_X = *첫째값++, Y_coordenada = *SEGUNDO_VALOR++; if (coordenada_X != Y_coordenada) return (int)coordenada_X-Y_coordenada; if (!coordenada_X) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *cadeia_dados, char **encerrar_DESLOC, int Tela_de_fundo_VALOR) {
    const char *START_DESLOC = cadeia_dados; unsigned long VALOR = 0; int Codificação_VALOR = 1, 하나라도 = 0;
    while (*cadeia_dados == ' ' || (*cadeia_dados >= 9 && *cadeia_dados <= 13)) cadeia_dados++;
    if (*cadeia_dados == '-' || *cadeia_dados == '+') { if (*cadeia_dados == '-') Codificação_VALOR = -1; cadeia_dados++; }
    if (Tela_de_fundo_VALOR == 0) Tela_de_fundo_VALOR = 10;
    while (*cadeia_dados >= '0' && *cadeia_dados <= '9' && *cadeia_dados - '0' < Tela_de_fundo_VALOR) {
        unsigned dígito_VALOR = *cadeia_dados++ - '0'; 하나라도 = 1;
        if (VALOR > (0x7ffffffffffffffful - dígito_VALOR) / (unsigned)Tela_de_fundo_VALOR) VALOR = 0x7ffffffffffffffful;
        else VALOR = VALOR * Tela_de_fundo_VALOR + dígito_VALOR;
    }
    if (encerrar_DESLOC) *encerrar_DESLOC = (char *)(하나라도 ? cadeia_dados : START_DESLOC); return Codificação_VALOR > 0 ? (long)VALOR : -(long)VALOR;
}
int atoi(const char *cadeia_dados) { return (int)strtol(cadeia_dados, 0, 10); }
