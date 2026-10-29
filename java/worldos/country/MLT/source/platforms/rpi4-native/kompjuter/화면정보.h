#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 attwali_data RGB32 화면 daqqas. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: moħbi_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void bord_pointer(int 가로, int Vertikali_pożizzjoni, unsigned forma_VALUE);
/* 한 번에 32줄을 완성한 Lura_VALUE, 달라진 화소만 attwali_data 화면에 옮긴다. */
void bord_Ħejji_tpinġija(volatile uint32_t *data, unsigned 폭, unsigned tul_VALUE, unsigned leading_VALUE);
int 보드그림범위(int *가로, int *Vertikali_pożizzjoni, int *폭, int *tul_VALUE);
int bord_Bidu_tpinġija(int 가로, int Vertikali_pożizzjoni, int 폭, int tul_VALUE);
void bord_Tmiem_tpinġija(void);
void 보드사각그림(int 가로, int Vertikali_pożizzjoni, int 폭, int tul_VALUE, uint32_t 색);
/* attwali_data wera_VALUE_487749b8 메모리에 기록한 pel 수. pointer 갱신은 제외한다. */
uint64_t bord_tpinġija_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Vertikali_pożizzjoni);
#endif
