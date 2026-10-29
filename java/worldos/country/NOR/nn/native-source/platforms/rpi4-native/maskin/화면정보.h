#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 faktisk_data RGB32 화면 Storleik. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Skjult_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Tavle_peikar(int 가로, int vertikalvising_plassere, unsigned figur_VALUE);
/* 한 번에 32줄을 완성한 TILBAKE_VALUE, 달라진 화소만 faktisk_data 화면에 옮긴다. */
void Tavle_Klargjer_teikning(volatile uint32_t *data, unsigned 폭, unsigned lengd_VALUE, unsigned lineavstand_VALUE);
int 보드그림범위(int *가로, int *vertikalvising_plassere, int *폭, int *lengd_VALUE);
int Tavle_START_teikning(int 가로, int vertikalvising_plassere, int 폭, int lengd_VALUE);
void Tavle_Ferdig_teikning(void);
void 보드사각그림(int 가로, int vertikalvising_plassere, int 폭, int lengd_VALUE, uint32_t 색);
/* faktisk_data vise_VALUE_487749b8 메모리에 기록한 piksel 수. peikar 갱신은 제외한다. */
uint64_t Tavle_teikning_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned vertikalvising_plassere);
#endif
