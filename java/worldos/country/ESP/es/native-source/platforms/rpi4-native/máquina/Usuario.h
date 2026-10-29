#ifndef encabezadoUsuarioNativo
#define encabezadoUsuarioNativo
#include <stdint.h>
#include <stddef.h>
#define baseUsuario 0x02000000ul
#define finImagenUsuario 0x02c00000ul
#define finMontículoUsuario 0x02ed0000ul
#define direcciónPilaUsuario 0x02f00000ul
#define finUsuario 0x03000000ul
#define númeroElementosPáginaUsuario ((finUsuario - baseUsuario) / 4096ul)
#define errorCódigoEjecutableUsuario (-8)
#define errorDatosUsuario (-1001)
#define errorEjecuciónUsuario (-1002)
#define instrucciónMáquinaInválidoUsuario (-1003)
#define tiempoEsperaUsuario (-1004)
#define interrumpidoUsuario (-1005)
typedef struct { uint64_t registroDatos[31], posiciónComando, códigoEstadoValor, direcciónPila; } marcoUsuario;
void operaciónInicializaciónSistemaUsuario(void);
int excepciónUsuario(marcoUsuario *, unsigned);
int eLFValidarUsuario(const unsigned char *, size_t);
uintptr_t ponerEnMarchaUsuarioPlaca(uintptr_t);
uintptr_t validarUsuarioPlaca(void);
uintptr_t controlUsuarioPlaca(uintptr_t);
uint32_t leerEstadoValorUsuario(unsigned, unsigned);
#endif
