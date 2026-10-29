#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 stvaran_podaci RGB32 화면 Veličina. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Skriveno_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void ploča_pokazivač(int 가로, int Vertikalno_položaj, unsigned oblik_VALUE);
/* 한 번에 32줄을 완성한 ZAD_VALUE, 달라진 화소만 stvaran_podaci 화면에 옮긴다. */
void ploča_Pripremiti_ucrtavanje(volatile uint32_t *podaci, unsigned 폭, unsigned dužina_VALUE, unsigned prored_VALUE);
int 보드그림범위(int *가로, int *Vertikalno_položaj, int *폭, int *dužina_VALUE);
int ploča_START_ucrtavanje(int 가로, int Vertikalno_položaj, int 폭, int dužina_VALUE);
void ploča_Kraj_ucrtavanje(void);
void 보드사각그림(int 가로, int Vertikalno_položaj, int 폭, int dužina_VALUE, uint32_t 색);
/* stvaran_podaci program_VALUE 메모리에 기록한 pel 수. pokazivač 갱신은 제외한다. */
uint64_t ploča_ucrtavanje_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Vertikalno_položaj);
#endif
