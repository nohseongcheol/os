#ifndef encabezadoLlamadaUsuarioNativo
#define encabezadoLlamadaUsuarioNativo
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=invocar número, x0..x5=argumentos, x0=resultado/valorNegativo error. Linux ABI 아님.
static inline intptr_t invocarUsuario(uintptr_t número, uintptr_t operandoPrimero, uintptr_t operandoSegundo, uintptr_t operandoTercero,
                                uintptr_t operandoCuarto, uintptr_t operandoQuinto, uintptr_t operandoSexto) {
    register uintptr_t registroCero __asm__("x0") = operandoPrimero;
    register uintptr_t registroUno __asm__("x1") = operandoSegundo;
    register uintptr_t registroDos __asm__("x2") = operandoTercero;
    register uintptr_t registroTres __asm__("x3") = operandoCuarto;
    register uintptr_t registroCuatro __asm__("x4") = operandoQuinto;
    register uintptr_t registroCinco __asm__("x5") = operandoSexto;
    register uintptr_t registroOcho __asm__("x8") = número;
    __asm__ volatile("svc #0" : "+r"(registroCero) : "r"(registroUno), "r"(registroDos), "r"(registroTres), "r"(registroCuatro), "r"(registroCinco), "r"(registroOcho) : "memory", "cc");
    return (intptr_t)registroCero;
}
static inline intptr_t rectánguloPantalla(unsigned coordenadaCoordenadaHorizontal, unsigned coordenadaCoordenadaVertical, unsigned valorAnchuraSolicitado, unsigned valorAlturaSolicitado, unsigned colorRGB) {
    return invocarUsuario(13, coordenadaCoordenadaHorizontal, coordenadaCoordenadaVertical, colorRGB, valorAnchuraSolicitado, valorAlturaSolicitado, 0);
}
static inline intptr_t finMemoriaUsuario(uintptr_t terminación) { return invocarUsuario(8, terminación, 0, 0, 0, 0, 0); }
static inline intptr_t leerAnchuraPantalla(void) { return invocarUsuario(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t leerAlturaPantalla(void) { return invocarUsuario(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t esperarTeclaPantallaPara(void) {
    intptr_t resultado = invocarUsuario(16, 0, 0, 0, 0, 0, 0);
    if (resultado < 0) return resultado;
    do { resultado = invocarUsuario(16, 1, 0, 0, 0, 0, 0); } while (resultado == -11);
    invocarUsuario(16, 2, 0, 0, 0, 0, 0);
    return resultado;
}
static inline intptr_t númeroElementosArgumentoUsuario(void) { return invocarUsuario(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t argumentoUsuario(unsigned número, char *valorContenidoValor, size_t tamaño) {
    return invocarUsuario(15, número, (uintptr_t)valorContenidoValor, tamaño, 0, 0, 0);
}
#endif
