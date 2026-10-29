#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 tényleges_adat RGB32 화면 Méret. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Rejtett_ÉRTÉK, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void fal_mutató(int 가로, int szektor_pozíció, unsigned alakzat_ÉRTÉK);
/* 한 번에 32줄을 완성한 BACK_ÉRTÉK, 달라진 화소만 tényleges_adat 화면에 옮긴다. */
void fal_Előkészítés_rajz(volatile uint32_t *adat, unsigned 폭, unsigned hossz_ÉRTÉK, unsigned sorköz_ÉRTÉK);
int 보드그림범위(int *가로, int *szektor_pozíció, int *폭, int *hossz_ÉRTÉK);
int fal_START_rajz(int 가로, int szektor_pozíció, int 폭, int hossz_ÉRTÉK);
void fal_Befejezés_rajz(void);
void fal_téglalap_kitöltés(int 가로, int szektor_pozíció, int 폭, int hossz_ÉRTÉK, uint32_t 색);
/* tényleges_adat bemutató_ÉRTÉK 메모리에 기록한 képpont szám. mutató 갱신은 제외한다. */
uint64_t fal_rajz_DARAB(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned szektor_pozíció);
#endif
