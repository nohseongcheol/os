#ifndef nativní_vzdálené_připojení_Nadpis
#define nativní_vzdálené_připojení_Nadpis
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Připravit_vzdálený(void);
void 원격살피기(void);
void vzdálený_výstup(unsigned char);
int vzdálený_vstup(void);
int novinky_vzdálený_vstup(const unsigned char *,unsigned);
uintptr_t Panel_stínový_provoz(uintptr_t,uintptr_t);
uintptr_t Panel_konec_vzdálený_příkaz(uintptr_t);
uintptr_t Panel_vzdálený_počkej(uintptr_t);
void 원격화면살피기(void);
int řízení_vzdálený_displej(unsigned);
#endif
