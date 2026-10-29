#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 фактик_мәгълүмат RGB32 화면 үлчәмен_үзгәртү. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: яшерен_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void такта_күрсәткеч(int 가로, int Вертикаль_урнаштыру, unsigned форма_VALUE);
/* 한 번에 32줄을 완성한 Артка_VALUE, 달라진 화소만 фактик_мәгълүмат 화면에 옮긴다. */
void такта_Әзерләү_сызым(volatile uint32_t *мәгълүмат, unsigned 폭, unsigned озынлык_VALUE, unsigned юлара_интервал_VALUE);
int 보드그림범위(int *가로, int *Вертикаль_урнаштыру, int *폭, int *озынлык_VALUE);
int такта_Start_сызым(int 가로, int Вертикаль_урнаштыру, int 폭, int озынлык_VALUE);
void такта_Әзер_сызым(void);
void 보드사각그림(int 가로, int Вертикаль_урнаштыру, int 폭, int озынлык_VALUE, uint32_t 색);
/* фактик_мәгълүмат күрсәтү_VALUE 메모리에 기록한 нокта 수. күрсәткеч 갱신은 제외한다. */
uint64_t такта_сызым_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Вертикаль_урнаштыру);
#endif
