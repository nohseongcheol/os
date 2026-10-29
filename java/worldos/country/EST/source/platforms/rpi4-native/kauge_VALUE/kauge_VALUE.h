#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Ettevalmistamine_kauge(void);
void 원격살피기(void);
void kauge_toodang(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t Tahvel_varikasutus(uintptr_t,uintptr_t);
uintptr_t Tahvel_lõpeta_kõne_kauge_käsk(uintptr_t);
uintptr_t Tahvel_kauge_Oota(uintptr_t);
void 원격화면살피기(void);
int meede_kauge_ekraan(unsigned);
#endif
