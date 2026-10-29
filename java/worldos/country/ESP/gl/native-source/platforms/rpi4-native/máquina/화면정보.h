#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 real_datos RGB32 화면 Tamaño. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Oculto_VALOR, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Panel_punteiro(int 가로, int Vertical_cargo, unsigned forma_VALOR);
/* 한 번에 32줄을 완성한 ATRÁS_VALOR, 달라진 화소만 real_datos 화면에 옮긴다. */
void 보드그림준비(volatile uint32_t *datos, unsigned 폭, unsigned duración_VALOR, unsigned espazamento_entre_liñas_VALOR);
int 보드그림범위(int *가로, int *Vertical_cargo, int *폭, int *duración_VALOR);
int 보드그림시작(int 가로, int Vertical_cargo, int 폭, int duración_VALOR);
void 보드그림마침(void);
void 보드사각그림(int 가로, int Vertical_cargo, int 폭, int duración_VALOR, uint32_t 색);
/* real_datos mostrar_VALOR 메모리에 기록한 píxel 수. punteiro 갱신은 제외한다. */
uint64_t 보드그림기록수(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Vertical_cargo);
#endif
