#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 benetako_datuak RGB32 화면 Tamaina. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Ezkutua_balio, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void arbel_erakusle(int 가로, int Bertikala_kargu, unsigned forma_balio);
/* 한 번에 32줄을 완성한 ATZERA_balio, 달라진 화소만 benetako_datuak 화면에 옮긴다. */
void 보드그림준비(volatile uint32_t *datuak, unsigned 폭, unsigned luzera_balio, unsigned lerroarte_balio);
int 보드그림범위(int *가로, int *Bertikala_kargu, int *폭, int *luzera_balio);
int 보드그림시작(int 가로, int Bertikala_kargu, int 폭, int luzera_balio);
void 보드그림마침(void);
void 보드사각그림(int 가로, int Bertikala_kargu, int 폭, int luzera_balio, uint32_t 색);
/* benetako_datuak erakutsi_balio 메모리에 기록한 pixel 수. erakusle 갱신은 제외한다. */
uint64_t 보드그림기록수(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Bertikala_kargu);
#endif
