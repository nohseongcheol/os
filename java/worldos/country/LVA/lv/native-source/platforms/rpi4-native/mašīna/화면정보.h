#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 faktisks_dati RGB32 화면 Izmērs. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Slēpts_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Panelis_rādītājs(int 가로, int vertikāle_amats, unsigned forma_VALUE);
/* 한 번에 32줄을 완성한 ATPAKAĻ_VALUE, 달라진 화소만 faktisks_dati 화면에 옮긴다. */
void Panelis_Sagatavot_zīmējums(volatile uint32_t *dati, unsigned 폭, unsigned 길이, unsigned rindstarpa_VALUE);
int 보드그림범위(int *가로, int *vertikāle_amats, int *폭, int *길이);
int Panelis_Sākt_zīmējums(int 가로, int vertikāle_amats, int 폭, int 길이);
void Panelis_beigas_zīmējums(void);
void Panelis_taisnstūris_aizpildīt(int 가로, int vertikāle_amats, int 폭, int 길이, uint32_t 색);
/* faktisks_dati rādīt_VALUE 메모리에 기록한 attēla_elements numurs. rādītājs 갱신은 제외한다. */
uint64_t Panelis_zīmējums_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned vertikāle_amats);
#endif
