#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 skutočný_údaje RGB32 화면 Veľkosť. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Skryté_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Panel_ukazovateľ(int 가로, int vertikála_pozícia, unsigned tvar_VALUE);
/* 한 번에 32줄을 완성한 BACK_VALUE, 달라진 화소만 skutočný_údaje 화면에 옮긴다. */
void Panel_Pripraviť_kresba(volatile uint32_t *údaje, unsigned 폭, unsigned dĺžka_VALUE, unsigned Riadkovanie_VALUE);
int 보드그림범위(int *가로, int *vertikála_pozícia, int *폭, int *dĺžka_VALUE);
int Panel_START_kresba(int 가로, int vertikála_pozícia, int 폭, int dĺžka_VALUE);
void Panel_Dokončiť_kresba(void);
void Panel_obdĺžnik_výplň(int 가로, int vertikála_pozícia, int 폭, int dĺžka_VALUE, uint32_t 색);
/* skutočný_údaje zobraziť_VALUE_487749b8 메모리에 기록한 pixel 수. ukazovateľ 갱신은 제외한다. */
uint64_t Panel_kresba_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned vertikála_pozícia);
#endif
