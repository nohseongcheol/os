#ifndef nativo_usuário_Ligar_Cabeçalho
#define nativo_usuário_Ligar_Cabeçalho
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 ÍNDICE, x0..x5=argumentos, x0=resultado/negativo_VALOR erro. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t ÍNDICE, uintptr_t 가, uintptr_t SEGUNDO_operando, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t registro_zero __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = SEGUNDO_operando;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = ÍNDICE;
    __asm__ volatile("svc #0" : "+r"(registro_zero) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)registro_zero;
}
static inline intptr_t tela_retângulo(unsigned coordenada_X, unsigned Y_coordenada, unsigned 너비값, unsigned solicitado_altura_VALOR, unsigned 빛삼원색) {
    return 사용자호출(13, coordenada_X, Y_coordenada, 빛삼원색, 너비값, solicitado_altura_VALOR, 0);
}
static inline intptr_t usuário_Memória_encerrar(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t leitura_tela_altura(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t resultado = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (resultado < 0) return resultado;
    do { resultado = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (resultado == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return resultado;
}
static inline intptr_t usuário_argumento_CONT_NÚM(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t usuário_argumento(unsigned ÍNDICE, char *Conteúdo_VALOR, size_t Tamanho) {
    return 사용자호출(15, ÍNDICE, (uintptr_t)Conteúdo_VALOR, Tamanho, 0, 0, 0);
}
#endif
