#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*inicializador_método)(void);
extern inicializador_método __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_usuário_app(int);
int usuário_START(int 전달값) {
    for (inicializador_método *dados_cargo = __init_array_start; dados_cargo < __init_array_end; dados_cargo++) (*dados_cargo)();
    int resultado = START_usuário_app(전달값);
    for (inicializador_método *dados_cargo = __fini_array_end; dados_cargo != __fini_array_start;) (*--dados_cargo)();
    return resultado;
}
void *memset(void *dados_cargo, int VALOR, size_t entrada_CONT_NÚM_8f7753a1) { unsigned char *destino_dados = dados_cargo; while (entrada_CONT_NÚM_8f7753a1--) *destino_dados++ = VALOR; return dados_cargo; }
void *memcpy(void *destino_dados, const void *cadeia_dados, size_t entrada_CONT_NÚM_8f7753a1) { unsigned char *첫째값 = destino_dados; const unsigned char *SEGUNDO_VALOR = cadeia_dados; while (entrada_CONT_NÚM_8f7753a1--) *첫째값++ = *SEGUNDO_VALOR++; return destino_dados; }
