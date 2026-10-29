#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Klargjer_fjern(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t Tavle_skygging(uintptr_t,uintptr_t);
uintptr_t Tavle_avslutte_fjern_kommando(uintptr_t);
uintptr_t Tavle_fjern_vent(uintptr_t);
void 원격화면살피기(void);
int styring_fjern_vise(unsigned);
#endif
