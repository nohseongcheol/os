#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_usuario_apl(int);
int usuario_START(int 전달값) {
    for (초기화함수 *datos_cargo = __init_array_start; datos_cargo < __init_array_end; datos_cargo++) (*datos_cargo)();
    int RESULTANTE = START_usuario_apl(전달값);
    for (초기화함수 *datos_cargo = __fini_array_end; datos_cargo != __fini_array_start;) (*--datos_cargo)();
    return RESULTANTE;
}
void *memset(void *datos_cargo, int VALOR, size_t introdución_CONTAR) { unsigned char *destino_datos = datos_cargo; while (introdución_CONTAR--) *destino_datos++ = VALOR; return datos_cargo; }
void *memcpy(void *destino_datos, const void *cadea_datos, size_t introdución_CONTAR) { unsigned char *첫째값 = destino_datos; const unsigned char *SEGUNDO_VALOR = cadea_datos; while (introdución_CONTAR--) *첫째값++ = *SEGUNDO_VALOR++; return destino_datos; }
