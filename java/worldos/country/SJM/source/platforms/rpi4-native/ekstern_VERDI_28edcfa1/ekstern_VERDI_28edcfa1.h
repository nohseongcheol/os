#ifndef opprinnelig_ekstern_tilkobling_Topptekst
#define opprinnelig_ekstern_tilkobling_Topptekst
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Forbered_ekstern(void);
void 원격살피기(void);
void ekstern_produksjon(unsigned char);
int ekstern_inndata(void);
int feed_ekstern_inndata(const unsigned char *,unsigned);
uintptr_t Tavle_skygging(uintptr_t,uintptr_t);
uintptr_t Tavle_avslutte_en_samtale_ekstern_kommando(uintptr_t);
uintptr_t Tavle_ekstern_vent(uintptr_t);
void 원격화면살피기(void);
int kontroll_ekstern_vise(unsigned);
#endif
