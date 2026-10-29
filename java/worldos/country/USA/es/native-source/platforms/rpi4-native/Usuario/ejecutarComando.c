#include "../denominación/nombresEnlazarMáquina.h"
#include "invocar.h"
typedef void (*métodoInicializador)(void);
extern métodoInicializador __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int iniciarProgramaUsuario(int);
int iniciarUsuario(int valorReenviado) {
    for (métodoInicializador *posiciónDatos = __init_array_start; posiciónDatos < __init_array_end; posiciónDatos++) (*posiciónDatos)();
    int resultado = iniciarProgramaUsuario(valorReenviado);
    for (métodoInicializador *posiciónDatos = __fini_array_end; posiciónDatos != __fini_array_start;) (*--posiciónDatos)();
    return resultado;
}
void *memset(void *posiciónDatos, int valor, size_t númeroElementosEntradaElemento) { unsigned char *datosDestino = posiciónDatos; while (númeroElementosEntradaElemento--) *datosDestino++ = valor; return posiciónDatos; }
void *memcpy(void *datosDestino, const void *datosCadena, size_t númeroElementosEntradaElemento) { unsigned char *valorPrimero = datosDestino; const unsigned char *valorSegundo = datosCadena; while (númeroElementosEntradaElemento--) *valorPrimero++ = *valorSegundo++; return datosDestino; }
