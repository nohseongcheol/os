#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 laatii_keɓe RGB32 화면 waylude_etannde. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: suuɗii_njaru, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void 보드포인터(int 가로, int 세로, unsigned tagoodi_njaru);
/* 한 번에 32줄을 완성한 Caggal_njaru, 달라진 화소만 laatii_keɓe 화면에 옮긴다. */
void 보드그림준비(volatile uint32_t *keɓe, unsigned 폭, unsigned njuuteendi_njaru, unsigned boowinol_gori_njaru);
int 보드그림범위(int *가로, int *세로, int *폭, int *njuuteendi_njaru);
int 보드그림시작(int 가로, int 세로, int 폭, int njuuteendi_njaru);
void 보드그림마침(void);
void 보드사각그림(int 가로, int 세로, int 폭, int njuuteendi_njaru, uint32_t 색);
/* laatii_keɓe hollirde_njaru 메모리에 기록한 piksel 수. 포인터 갱신은 제외한다. */
uint64_t 보드그림기록수(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned 세로);
#endif
