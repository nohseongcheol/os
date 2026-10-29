#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 skutečný_data RGB32 화면 Velikost. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Skrytý_HODNOTA, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Panel_ukazatel(int 가로, int Svislá_pozice, unsigned tvar_HODNOTA);
/* 한 번에 32줄을 완성한 BACK_HODNOTA, 달라진 화소만 skutečný_data 화면에 옮긴다. */
void Panel_Připravit_kreslení(volatile uint32_t *data, unsigned 폭, unsigned délka_HODNOTA, unsigned řádkování_HODNOTA);
int 보드그림범위(int *가로, int *Svislá_pozice, int *폭, int *délka_HODNOTA);
int Panel_START_kreslení(int 가로, int Svislá_pozice, int 폭, int délka_HODNOTA);
void Panel_Dokončit_kreslení(void);
void Panel_obdélník_výplň(int 가로, int Svislá_pozice, int 폭, int délka_HODNOTA, uint32_t 색);
/* skutečný_data zobrazit_HODNOTA 메모리에 기록한 pixel číslo. ukazatel 갱신은 제외한다. */
uint64_t Panel_kreslení_POČET(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Svislá_pozice);
#endif
