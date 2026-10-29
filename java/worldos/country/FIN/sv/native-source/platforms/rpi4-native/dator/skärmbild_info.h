#ifndef ursprunglig_skärmbild_info_huvud
#define ursprunglig_skärmbild_info_huvud
#include <stdint.h>
/* 초기화가 끝난 verklig_data RGB32 skärmbild Storlek. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Dold_värde, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Tavla_markör(int 가로, int bransch_placera, unsigned form_värde);
/* 한 번에 32줄을 완성한 BACK_värde, 달라진 화소만 verklig_data 화면에 옮긴다. */
void Tavla_Förbereda_ritning(volatile uint32_t *data, unsigned 폭, unsigned längd_värde, unsigned avstånd_värde);
int 보드그림범위(int *가로, int *bransch_placera, int *폭, int *längd_värde);
int Tavla_START_ritning(int 가로, int bransch_placera, int 폭, int längd_värde);
void Tavla_slut_ritning(void);
void Tavla_rektangel_Fyll(int 가로, int bransch_placera, int 폭, int längd_värde, uint32_t 색);
/* verklig_data visa_värde 메모리에 기록한 bildpunkt nummer. markör 갱신은 제외한다. */
uint64_t Tavla_ritning_ANTAL(void);
uint32_t Tavla_läsa_skärmbild(unsigned 가로, unsigned bransch_placera);
#endif
