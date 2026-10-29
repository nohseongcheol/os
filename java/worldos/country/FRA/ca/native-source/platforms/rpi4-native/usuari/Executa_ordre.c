#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Inici_usuari_programa(int);
int usuari_Inici(int 전달값) {
    for (초기화함수 *dades_càrrec = __init_array_start; dades_càrrec < __init_array_end; dades_càrrec++) (*dades_càrrec)();
    int RESULTAT = Inici_usuari_programa(전달값);
    for (초기화함수 *dades_càrrec = __fini_array_end; dades_càrrec != __fini_array_start;) (*--dades_càrrec)();
    return RESULTAT;
}
void *memset(void *dades_càrrec, int VALOR, size_t introducció_COMPT) { unsigned char *destinació_dades = dades_càrrec; while (introducció_COMPT--) *destinació_dades++ = VALOR; return dades_càrrec; }
void *memcpy(void *destinació_dades, const void *cadena_dades, size_t introducció_COMPT) { unsigned char *첫째값 = destinació_dades; const unsigned char *SEGON_VALOR = cadena_dades; while (introducció_COMPT--) *첫째값++ = *SEGON_VALOR++; return destinació_dades; }
