#ifndef systeemeigen_scherm_info_header
#define systeemeigen_scherm_info_header
#include <stdint.h>
/* 초기화가 끝난 werkelijk_gegevens RGB32 scherm Grootte. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t Bord_scherm_hoogte(void);
/* 0: Verborgen_WAARDE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Bord_wijzer(int 가로, int Verticaal_functie, unsigned vorm_WAARDE);
/* 한 번에 32줄을 완성한 BACK_WAARDE, 달라진 화소만 werkelijk_gegevens 화면에 옮긴다. */
void Bord_Bereid_voor_tekening(volatile uint32_t *gegevens, unsigned 폭, unsigned tijdsduur_WAARDE, unsigned interlinie_WAARDE);
int 보드그림범위(int *가로, int *Verticaal_functie, int *폭, int *tijdsduur_WAARDE);
int Bord_START_tekening(int 가로, int Verticaal_functie, int 폭, int tijdsduur_WAARDE);
void Bord_Voltooien_tekening(void);
void Bord_rechthoek_vullen(int 가로, int Verticaal_functie, int 폭, int tijdsduur_WAARDE, uint32_t 색);
/* werkelijk_gegevens weergeven_WAARDE 메모리에 기록한 pixel nummer. wijzer 갱신은 제외한다. */
uint64_t Bord_tekening_AANTAL(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Verticaal_functie);
#endif
