#ifndef encabezadoConexiónRemotoNativo
#define encabezadoConexiónRemotoNativo
#include "../denominación/nombresEnlazarMáquina.h"
#include <stdint.h>
void prepararRemoto(void);
void inspeccionarRemoto(void);
void salidaRemoto(unsigned char);
int entradaRemoto(void);
int entradaRemotoAlimentar(const unsigned char *,unsigned);
uintptr_t controlRemotoPlaca(uintptr_t,uintptr_t);
uintptr_t comandoRemotoFinPlaca(uintptr_t);
uintptr_t esperarRemotoPlaca(uintptr_t);
void inspeccionarPresentarRemoto(void);
int presentarRemotoControl(unsigned);
#endif
