#ifndef 자체화면정보머리
#define 자체화면정보머리
#include <stdint.h>
/* 초기화가 끝난 rzeczywisty_dane RGB32 화면 Rozmiar. 준비되지 않았으면 0이다. */
uintptr_t 보드화면너비(void);
uintptr_t 보드화면높이(void);
/* 0: Ukryty_WARTOŚĆ, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void Tablica_wskaźnik(int 가로, int gałąź_stanowisko, unsigned kształt_WARTOŚĆ);
/* 한 번에 32줄을 완성한 BACK_WARTOŚĆ, 달라진 화소만 rzeczywisty_dane 화면에 옮긴다. */
void Tablica_Przygotuj_rysunek(volatile uint32_t *dane, unsigned 폭, unsigned długość_WARTOŚĆ, unsigned interlinia_WARTOŚĆ);
int 보드그림범위(int *가로, int *gałąź_stanowisko, int *폭, int *długość_WARTOŚĆ);
int Tablica_START_rysunek(int 가로, int gałąź_stanowisko, int 폭, int długość_WARTOŚĆ);
void Tablica_Zakończ_rysunek(void);
void Tablica_prostokąt_Wypełnij(int 가로, int gałąź_stanowisko, int 폭, int długość_WARTOŚĆ, uint32_t 색);
/* rzeczywisty_dane program_WARTOŚĆ 메모리에 기록한 piksel identyfikator. wskaźnik 갱신은 제외한다. */
uint64_t Tablica_rysunek_ILE_LICZB(void);
uint32_t 보드화면읽기(unsigned 가로, unsigned gałąź_stanowisko);
#endif
