#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 tūturu_raraunga RGB32 화면 rahi. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: hunahuna_uara, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void papa_atatohu(int 가로, int Poutū_tūranga, unsigned hanga_uara);
/* 한 번에 32줄을 완성한 Hoki_uara, 달라진 화소만 tūturu_raraunga 화면에 옮긴다. */
void papa_Whakarite_tātuhi(volatile uint32_t *raraunga, unsigned 폭, unsigned roa_uara, unsigned mokowā_raina_uara);
int 보드그림범위(int *가로, int *Poutū_tūranga, int *폭, int *roa_uara);
int papa_Start_tātuhi(int 가로, int Poutū_tūranga, int 폭, int roa_uara);
void papa_Mutu_tātuhi(void);
void 보드사각그림(int 가로, int Poutū_tūranga, int 폭, int roa_uara, uint32_t 색);
/* tūturu_raraunga whakaatu_uara 메모리에 기록한 pika 수. atatohu 갱신은 제외한다. */
uint64_t papa_tātuhi_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Poutū_tūranga);
#endif
