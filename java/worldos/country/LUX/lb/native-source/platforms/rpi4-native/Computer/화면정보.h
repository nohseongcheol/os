#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 aktuell_Daten RGB32 화면 d_Gréisst_veränneren. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: verstoppt_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Board_Uweiser(int 가로, int Vertikal_positionéieren, unsigned Form_VALUE);
/* 한 번에 32줄을 완성한 Zeréck_VALUE, 달라진 화소만 aktuell_Daten 화면에 옮긴다. */
void Board_Préparéieren_Zeechnung(volatile uint32_t *Daten, unsigned 폭, unsigned Längt_VALUE, unsigned Anzuch_VALUE);
int 보드그림범위(int *가로, int *Vertikal_positionéieren, int *폭, int *Längt_VALUE);
int Board_Start_Zeechnung(int 가로, int Vertikal_positionéieren, int 폭, int Längt_VALUE);
void Board_Ofschléissen_Zeechnung(void);
void 보드사각그림(int 가로, int Vertikal_positionéieren, int 폭, int Längt_VALUE, uint32_t 색);
/* aktuell_Daten Show_VALUE 메모리에 기록한 Pel 수. Uweiser 갱신은 제외한다. */
uint64_t Board_Zeechnung_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Vertikal_positionéieren);
#endif
