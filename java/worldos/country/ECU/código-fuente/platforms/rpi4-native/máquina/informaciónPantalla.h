#ifndef encabezadoInformaciónPantallaNativo
#define encabezadoInformaciónPantallaNativo
#include <stdint.h>
/* 초기화가 끝난 datosEfectivo RGB32 Pantalla tamaño. 준비되지 않았으면 0이다. */
uintptr_t anchuraPantallaPlaca(void);
uintptr_t alturaPantallaPlaca(void);
/* 0: valorOculto, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void punteroPlaca(int posiciónHorizontal, int posiciónVertical, unsigned valorForma);
/* 한 번에 32줄을 완성한 valorLadoPosterior, 달라진 화소만 datosEfectivo 화면에 옮긴다. */
void dibujoPrepararPlaca(volatile uint32_t *Datos, unsigned extensiónRangoAnchura, unsigned longitud, unsigned valorEspaciadoLínea);
int límitesDibujoPlaca(int *posiciónHorizontal, int *posiciónVertical, int *extensiónRangoAnchura, int *longitud);
int dibujoIniciarPlaca(int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int longitud);
void dibujoTerminarPlaca(void);
void rellenarRectánguloPlaca(int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int longitud, uint32_t valorColor);
/* datosEfectivo mostrarValor 메모리에 기록한 píxel númeroValor. puntero 갱신은 제외한다. */
uint64_t númeroElementosDibujoPlaca(void);
uint32_t pantallaLeerPlaca(unsigned posiciónHorizontal, unsigned posiciónVertical);
#endif
