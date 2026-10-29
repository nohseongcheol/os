#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 اصلي_ڪوائف RGB32 화면 سائيز. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: ڳجهو_قدر, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void 보드포인터(int 가로, int 세로, unsigned شڪل_قدر);
/* 한 번에 32줄을 완성한 واپس_قدر, 달라진 화소만 اصلي_ڪوائف 화면에 옮긴다. */
void 보드그림준비(volatile uint32_t *ڪوائف, unsigned 폭, unsigned لمبائي_قدر, unsigned اڳواڻي_قدر);
int 보드그림범위(int *가로, int *세로, int *폭, int *لمبائي_قدر);
int 보드그림시작(int 가로, int 세로, int 폭, int لمبائي_قدر);
void 보드그림마침(void);
void 보드사각그림(int 가로, int 세로, int 폭, int لمبائي_قدر, uint32_t 색);
/* اصلي_ڪوائف نمائش_ڪريو_قدر 메모리에 기록한 پيل 수. پوائنٽر 갱신은 제외한다. */
uint64_t 보드그림기록수(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned 세로);
#endif
