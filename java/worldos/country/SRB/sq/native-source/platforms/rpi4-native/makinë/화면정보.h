#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 aktual_të_dhëna RGB32 화면 Madhësi. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: i_fshehur_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void panel_tregues(int 가로, int Vertikal_pozicioni, unsigned formë_VALUE);
/* 한 번에 32줄을 완성한 PAS_VALUE, 달라진 화소만 aktual_të_dhëna 화면에 옮긴다. */
void panel_Përgatit_vizatim(volatile uint32_t *të_dhëna, unsigned 폭, unsigned gjatësi_VALUE, unsigned hapësira_midis_rreshtave_VALUE);
int 보드그림범위(int *가로, int *Vertikal_pozicioni, int *폭, int *gjatësi_VALUE);
int panel_nis_vizatim(int 가로, int Vertikal_pozicioni, int 폭, int gjatësi_VALUE);
void panel_Përfundo_vizatim(void);
void 보드사각그림(int 가로, int Vertikal_pozicioni, int 폭, int gjatësi_VALUE, uint32_t 색);
/* aktual_të_dhëna shfaq_VALUE 메모리에 기록한 pikëz 수. tregues 갱신은 제외한다. */
uint64_t panel_vizatim_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Vertikal_pozicioni);
#endif
