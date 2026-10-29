#ifndef systemnahBildschirmInformationKopf
#define systemnahBildschirmInformationKopf
#include <stdint.h>
/* 초기화가 끝난 tatsächlichDaten RGB32 Bildschirm größe. 준비되지 않았으면 0이다. */
uintptr_t platineBildschirmBreite(void);
uintptr_t platineBildschirmHöhe(void);
/* 0: verborgenWert, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void platineZeiger(int waagerechtPosition, int senkrechtPosition, unsigned formWert);
/* 한 번에 32줄을 완성한 rückseiteWert, 달라진 화소만 tatsächlichDaten 화면에 옮긴다. */
void platineVorbereitenZeichnung(volatile uint32_t *Daten, unsigned breiteSpannweite, unsigned Länge, unsigned zeileAbstandWert);
int platineZeichnungGrenzen(int *waagerechtPosition, int *senkrechtPosition, int *breiteSpannweite, int *Länge);
int platineStartenZeichnung(int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int Länge);
void platineBeendenZeichnung(void);
void platineRechteckFüllen(int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int Länge, uint32_t farbeWert);
/* tatsächlichDaten wertAnzeigen 메모리에 기록한 bildpunkt Zahl. zeiger 갱신은 제외한다. */
uint64_t platineZeichnungAnzahl(void);
uint32_t platineLesenBildschirm(unsigned waagerechtPosition, unsigned senkrechtPosition);
#endif
