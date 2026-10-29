#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Pripraviť_vzdialený(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int vzdialený_vstup(void);
int súhrnný_obsah_vzdialený_vstup(const unsigned char *,unsigned);
uintptr_t Panel_tieňové_ovládanie(uintptr_t,uintptr_t);
uintptr_t Panel_ukončiť_hovor_vzdialený_príkaz(uintptr_t);
uintptr_t Panel_vzdialený_počkaj(uintptr_t);
void 원격화면살피기(void);
int riadenie_vzdialený_displej(unsigned);
#endif
