#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 real_dades RGB32 화면 Mida. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Amagat_VALOR, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Tauler_punter(int 가로, int Vertical_càrrec, unsigned forma_VALOR);
/* 한 번에 32줄을 완성한 ENRERE_VALOR, 달라진 화소만 real_dades 화면에 옮긴다. */
void Tauler_Prepara_dibuix(volatile uint32_t *dades, unsigned 폭, unsigned durada_VALOR, unsigned interlineat_VALOR);
int 보드그림범위(int *가로, int *Vertical_càrrec, int *폭, int *durada_VALOR);
int Tauler_Inici_dibuix(int 가로, int Vertical_càrrec, int 폭, int durada_VALOR);
void Tauler_fi_dibuix(void);
void 보드사각그림(int 가로, int Vertical_càrrec, int 폭, int durada_VALOR, uint32_t 색);
/* real_dades mostrar_VALOR 메모리에 기록한 píxel 수. punter 갱신은 제외한다. */
uint64_t Tauler_dibuix_COMPT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Vertical_càrrec);
#endif
