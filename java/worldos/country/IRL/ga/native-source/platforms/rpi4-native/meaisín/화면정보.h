#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 iarbhír_sonraí RGB32 화면 Méid. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: folaithe_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void clár_pointeoir(int 가로, int Ingearach_suíomh, unsigned cruth_VALUE);
/* 한 번에 32줄을 완성한 Siar_VALUE, 달라진 화소만 iarbhír_sonraí 화면에 옮긴다. */
void clár_Ullmhaigh_líníocht(volatile uint32_t *sonraí, unsigned 폭, unsigned fad_VALUE, unsigned spásáil_línte_VALUE);
int 보드그림범위(int *가로, int *Ingearach_suíomh, int *폭, int *fad_VALUE);
int clár_Start_líníocht(int 가로, int Ingearach_suíomh, int 폭, int fad_VALUE);
void clár_Críochnaigh_líníocht(void);
void 보드사각그림(int 가로, int Ingearach_suíomh, int 폭, int fad_VALUE, uint32_t 색);
/* iarbhír_sonraí seó_VALUE 메모리에 기록한 picteilín 수. pointeoir 갱신은 제외한다. */
uint64_t clár_líníocht_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Ingearach_suíomh);
#endif
