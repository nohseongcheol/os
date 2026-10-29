#ifndef opprinnelig_skjermbilde_info_Topptekst
#define opprinnelig_skjermbilde_info_Topptekst
#include <stdint.h>
/* 초기화가 끝난 faktisk_data RGB32 skjermbilde Størrelse. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Skjult_VERDI, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Tavle_peker(int 가로, int vertikal_plassere, unsigned figur_VERDI);
/* 한 번에 32줄을 완성한 TILBAKE_VERDI, 달라진 화소만 faktisk_data 화면에 옮긴다. */
void Tavle_Forbered_tegning(volatile uint32_t *data, unsigned 폭, unsigned lengde_VERDI, unsigned linjeavstand_VERDI);
int 보드그림범위(int *가로, int *vertikal_plassere, int *폭, int *lengde_VERDI);
int Tavle_START_tegning(int 가로, int vertikal_plassere, int 폭, int lengde_VERDI);
void Tavle_slutt_tegning(void);
void Tavle_rektangel_fyll(int 가로, int vertikal_plassere, int 폭, int lengde_VERDI, uint32_t 색);
/* faktisk_data vise_VERDI_487749b8 메모리에 기록한 piksel nummer. peker 갱신은 제외한다. */
uint64_t Tavle_tegning_ANTALL(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned vertikal_plassere);
#endif
