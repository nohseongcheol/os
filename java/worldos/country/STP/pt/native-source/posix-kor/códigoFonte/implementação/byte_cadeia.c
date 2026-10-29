#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *cadeia_VALOR) { size_t duração_VALOR = 0; while (cadeia_VALOR[duração_VALOR]) duração_VALOR++; return duração_VALOR; }
int strcmp(const char *câmera_frontal_VALOR, const char *BACK_VALOR) {
    while (*câmera_frontal_VALOR && *câmera_frontal_VALOR == *BACK_VALOR) { câmera_frontal_VALOR++; BACK_VALOR++; }
    return (unsigned char)*câmera_frontal_VALOR - (unsigned char)*BACK_VALOR;
}
int memcmp(const void *câmera_frontal_VALOR, const void *BACK_VALOR, size_t byte_CONT_NÚM) {
    const unsigned char *가 = câmera_frontal_VALOR, *SEGUNDO_operando = BACK_VALOR;
    for (size_t slot_entrada = 0; slot_entrada < byte_CONT_NÚM; slot_entrada++) if (가[slot_entrada] != SEGUNDO_operando[slot_entrada]) return 가[slot_entrada] - SEGUNDO_operando[slot_entrada];
    return 0;
}
void *memcpy(void *destino_VALOR, const void *원본, size_t byte_CONT_NÚM) {
    unsigned char *가 = destino_VALOR; const unsigned char *SEGUNDO_operando = 원본;
    for (size_t slot_entrada = 0; slot_entrada < byte_CONT_NÚM; slot_entrada++) 가[slot_entrada] = SEGUNDO_operando[slot_entrada];
    return destino_VALOR;
}
void *memset(void *destino_VALOR, int VALOR, size_t byte_CONT_NÚM) {
    unsigned char *dados = destino_VALOR;
    for (size_t slot_entrada = 0; slot_entrada < byte_CONT_NÚM; slot_entrada++) dados[slot_entrada] = VALOR;
    return destino_VALOR;
}
int putchar(int 문자) { unsigned char VALOR = 문자; return write(1, &VALOR, 1) == 1 ? VALOR : EOF; }
int puts(const char *cadeia_VALOR) {
    size_t duração_VALOR = strlen(cadeia_VALOR), posição = 0;
    while (posição < duração_VALOR) { ssize_t resultado = write(1, cadeia_VALOR + posição, duração_VALOR - posição); if (resultado <= 0) return EOF; posição += resultado; }
    return putchar('\n') == EOF ? EOF : 0;
}
