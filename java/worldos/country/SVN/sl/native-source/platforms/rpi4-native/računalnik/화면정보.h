#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 dejanski_podatki RGB32 화면 Velikost. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Skrito_VALUE, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Tabla_kazalec(int 가로, int Navpično_položaj, unsigned oblika_VALUE_f1cd655a);
/* 한 번에 32줄을 완성한 ZAJ_VALUE, 달라진 화소만 dejanski_podatki 화면에 옮긴다. */
void Tabla_Pripravi_risba(volatile uint32_t *podatki, unsigned 폭, unsigned 길이, unsigned razmik_vrstic_VALUE);
int 보드그림범위(int *가로, int *Navpično_položaj, int *폭, int *길이);
int Tabla_Start_risba(int 가로, int Navpično_položaj, int 폭, int 길이);
void Tabla_konec_risba(void);
void Tabla_pravokotnik_polnilo(int 가로, int Navpično_položaj, int 폭, int 길이, uint32_t 색);
/* dejanski_podatki oddaja_VALUE_487749b8 메모리에 기록한 slikovna_pika 수. kazalec 갱신은 제외한다. */
uint64_t Tabla_risba_COUNT(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned Navpično_položaj);
#endif
