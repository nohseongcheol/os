#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Pripravi_oddaljen(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t Tabla_oddaljeni_nadzor(uintptr_t,uintptr_t);
uintptr_t Tabla_končati_klic_oddaljen_ukaz(uintptr_t);
uintptr_t Tabla_oddaljen_počakaj(uintptr_t);
void 원격화면살피기(void);
int nadzor_oddaljen_zaslon(unsigned);
#endif
