#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 totoo_data RGB32 화면 sukat_82232621. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: nakatago_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void board_pointer(int 가로, int archive_posisyon, unsigned hugis_VALUE);
/* 한 번에 32줄을 완성한 Bumalik_VALUE, 달라진 화소만 totoo_data 화면에 옮긴다. */
void board_Ihanda_iginuhit(volatile uint32_t *data, unsigned 폭, unsigned haba_VALUE, unsigned pagitan_ng_linya_VALUE);
int 보드그림범위(int *가로, int *archive_posisyon, int *폭, int *haba_VALUE);
int board_Start_iginuhit(int 가로, int archive_posisyon, int 폭, int haba_VALUE);
void board_Tapos_Na_iginuhit(void);
void 보드사각그림(int 가로, int archive_posisyon, int 폭, int haba_VALUE, uint32_t 색);
/* totoo_data ipakita_VALUE 메모리에 기록한 pel 수. pointer 갱신은 제외한다. */
uint64_t board_iginuhit_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned archive_posisyon);
#endif
