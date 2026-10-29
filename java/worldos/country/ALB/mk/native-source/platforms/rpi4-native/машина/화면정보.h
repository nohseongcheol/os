#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 реален_податоци RGB32 화면 Големина. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: скриен_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void табла_покажувач(int 가로, int вертикала_позиционирање, unsigned форма_VALUE);
/* 한 번에 32줄을 완성한 Назад_VALUE, 달라진 화소만 реален_податоци 화면에 옮긴다. */
void табла_Подготви_цртеж(volatile uint32_t *податоци, unsigned 폭, unsigned должина_VALUE, unsigned проред_VALUE);
int 보드그림범위(int *가로, int *вертикала_позиционирање, int *폭, int *должина_VALUE);
int табла_Start_цртеж(int 가로, int вертикала_позиционирање, int 폭, int должина_VALUE);
void табла_Крај_цртеж(void);
void 보드사각그림(int 가로, int вертикала_позиционирање, int 폭, int должина_VALUE, uint32_t 색);
/* реален_податоци прикажи_VALUE 메모리에 기록한 пиксел 수. покажувач 갱신은 제외한다. */
uint64_t табла_цртеж_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned вертикала_позиционирање);
#endif
