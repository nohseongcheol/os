#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 werklik_data RGB32 화면 Grootte. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: verskuilde_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void bord_wyser(int 가로, int Vertikaal_plaas, unsigned vorm_VALUE);
/* 한 번에 32줄을 완성한 TERUG_VALUE, 달라진 화소만 werklik_data 화면에 옮긴다. */
void bord_Maak_gereed_tekening(volatile uint32_t *data, unsigned 폭, unsigned lengte_VALUE, unsigned reëlspasiëring_VALUE);
int 보드그림범위(int *가로, int *Vertikaal_plaas, int *폭, int *lengte_VALUE);
int bord_BEGIN_tekening(int 가로, int Vertikaal_plaas, int 폭, int lengte_VALUE);
void bord_Klaar_tekening(void);
void 보드사각그림(int 가로, int Vertikaal_plaas, int 폭, int lengte_VALUE, uint32_t 색);
/* werklik_data wys_VALUE 메모리에 기록한 pieksel 수. wyser 갱신은 제외한다. */
uint64_t bord_tekening_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Vertikaal_plaas);
#endif
