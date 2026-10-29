#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 faktinis_duomenys RGB32 화면 Dydis. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Paslėptas_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Lenta_rodyklė(int 가로, int segmentas_padėtis, unsigned figūra_VALUE);
/* 한 번에 32줄을 완성한 ATGAL_VALUE, 달라진 화소만 faktinis_duomenys 화면에 옮긴다. */
void Lenta_Parengti_piešinys(volatile uint32_t *duomenys, unsigned 폭, unsigned 길이, unsigned eilučių_intervalas_VALUE);
int 보드그림범위(int *가로, int *segmentas_padėtis, int *폭, int *길이);
int Lenta_Start_piešinys(int 가로, int segmentas_padėtis, int 폭, int 길이);
void Lenta_Baigti_piešinys(void);
void Lenta_stačiakampis_užpildas(int 가로, int segmentas_padėtis, int 폭, int 길이, uint32_t 색);
/* faktinis_duomenys laida_VALUE 메모리에 기록한 pikselis numeris. rodyklė 갱신은 제외한다. */
uint64_t Lenta_piešinys_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned segmentas_padėtis);
#endif
