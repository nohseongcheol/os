#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 dearbh_dàta RGB32 화면 atharraich_am_meud. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: falaichte_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void bòrd_tomhaire(int 가로, int inghearach_suidhich, unsigned cruth_VALUE);
/* 한 번에 32줄을 완성한 Air_ais_VALUE, 달라진 화소만 dearbh_dàta 화면에 옮긴다. */
void bòrd_Ullaich_tarraing(volatile uint32_t *dàta, unsigned 폭, unsigned faid_VALUE, unsigned beàrn_eadar_dà_loidhne_VALUE);
int 보드그림범위(int *가로, int *inghearach_suidhich, int *폭, int *faid_VALUE);
int bòrd_Start_tarraing(int 가로, int inghearach_suidhich, int 폭, int faid_VALUE);
void bòrd_Coilean_tarraing(void);
void 보드사각그림(int 가로, int inghearach_suidhich, int 폭, int faid_VALUE, uint32_t 색);
/* dearbh_dàta show_VALUE 메모리에 기록한 pel 수. tomhaire 갱신은 제외한다. */
uint64_t bòrd_tarraing_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned inghearach_suidhich);
#endif
