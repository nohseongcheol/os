#ifndef oprindelig_skærmbillede_info_Header
#define oprindelig_skærmbillede_info_Header
#include <stdint.h>
/* 초기화가 끝난 faktisk_data RGB32 skærmbillede Størrelse. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Skjult_VÆRDI, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Tavle_markør(int 가로, int Lodret_placere, unsigned figur_VÆRDI);
/* 한 번에 32줄을 완성한 BACK_VÆRDI, 달라진 화소만 faktisk_data 화면에 옮긴다. */
void Tavle_Tilrettelæg_tegning(volatile uint32_t *data, unsigned 폭, unsigned varighed_VÆRDI, unsigned skydning_VÆRDI);
int 보드그림범위(int *가로, int *Lodret_placere, int *폭, int *varighed_VÆRDI);
int Tavle_START_tegning(int 가로, int Lodret_placere, int 폭, int varighed_VÆRDI);
void Tavle_Udfør_tegning(void);
void Tavle_rektangel_udfyld(int 가로, int Lodret_placere, int 폭, int varighed_VÆRDI, uint32_t 색);
/* faktisk_data vise_VÆRDI 메모리에 기록한 pixel tal. markør 갱신은 제외한다. */
uint64_t Tavle_tegning_TÆL(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Lodret_placere);
#endif
