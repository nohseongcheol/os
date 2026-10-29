#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 raun_gögn RGB32 화면 Stærð. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: falið_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void bretti_bendill(int 가로, int Lóðrétt_staða, unsigned form_VALUE);
/* 한 번에 32줄을 완성한 TIL_BAKA_VALUE, 달라진 화소만 raun_gögn 화면에 옮긴다. */
void bretti_Undirbúa_teikning(volatile uint32_t *gögn, unsigned 폭, unsigned lengd_VALUE, unsigned línubil_VALUE);
int 보드그림범위(int *가로, int *Lóðrétt_staða, int *폭, int *lengd_VALUE);
int bretti_Opna_teikning(int 가로, int Lóðrétt_staða, int 폭, int lengd_VALUE);
void bretti_Ljúka_teikning(void);
void 보드사각그림(int 가로, int Lóðrétt_staða, int 폭, int lengd_VALUE, uint32_t 색);
/* raun_gögn sýna_VALUE 메모리에 기록한 díll númer. bendill 갱신은 제외한다. */
uint64_t bretti_teikning_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Lóðrétt_staða);
#endif
