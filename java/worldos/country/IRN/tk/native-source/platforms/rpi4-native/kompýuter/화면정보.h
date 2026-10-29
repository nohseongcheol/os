#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 hakyky_maglumat RGB32 화면 Ululyk. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: gizlin_baha, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void 보드포인터(int 가로, int 세로, unsigned şekil_baha);
/* 한 번에 32줄을 완성한 Yza_baha, 달라진 화소만 hakyky_maglumat 화면에 옮긴다. */
void 보드그림준비(volatile uint32_t *maglumat, unsigned 폭, unsigned dowamlylyk_baha, unsigned setirara_baha);
int 보드그림범위(int *가로, int *세로, int *폭, int *dowamlylyk_baha);
int 보드그림시작(int 가로, int 세로, int 폭, int dowamlylyk_baha);
void 보드그림마침(void);
void 보드사각그림(int 가로, int 세로, int 폭, int dowamlylyk_baha, uint32_t 색);
/* hakyky_maglumat görkez_baha_487749b8 메모리에 기록한 pel 수. görkeziji 갱신은 제외한다. */
uint64_t 보드그림기록수(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned 세로);
#endif
