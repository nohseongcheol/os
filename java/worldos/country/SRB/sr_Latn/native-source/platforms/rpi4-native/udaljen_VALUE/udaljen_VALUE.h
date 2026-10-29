#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Pripremi_udaljen(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t Tabla_daljinska_kontrola(uintptr_t,uintptr_t);
uintptr_t Tabla_završiti_razgovor_udaljen_komanda(uintptr_t);
uintptr_t Tabla_udaljen_čekaj(uintptr_t);
void 원격화면살피기(void);
int kontrola_udaljen_ekran(unsigned);
#endif
