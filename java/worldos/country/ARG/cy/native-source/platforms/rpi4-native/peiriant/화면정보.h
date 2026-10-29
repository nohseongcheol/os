#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 go_iawn_data RGB32 화면 Maint. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: cudd_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void bwrdd_pwyntydd(int 가로, int Ar_i_fyny_safle, unsigned siâp_VALUE);
/* 한 번에 32줄을 완성한 BACK_VALUE, 달라진 화소만 go_iawn_data 화면에 옮긴다. */
void bwrdd_Paratoi_lluniad(volatile uint32_t *data, unsigned 폭, unsigned hyd_VALUE, unsigned rhynglinellu_VALUE);
int 보드그림범위(int *가로, int *Ar_i_fyny_safle, int *폭, int *hyd_VALUE);
int bwrdd_START_lluniad(int 가로, int Ar_i_fyny_safle, int 폭, int hyd_VALUE);
void bwrdd_Gorffen_lluniad(void);
void 보드사각그림(int 가로, int Ar_i_fyny_safle, int 폭, int hyd_VALUE, uint32_t 색);
/* go_iawn_data sioe_VALUE 메모리에 기록한 pel 수. pwyntydd 갱신은 제외한다. */
uint64_t bwrdd_lluniad_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Ar_i_fyny_safle);
#endif
