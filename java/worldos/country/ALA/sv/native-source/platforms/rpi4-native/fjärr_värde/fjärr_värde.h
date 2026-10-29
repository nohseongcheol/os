#ifndef ursprunglig_fjärranslutning_huvud
#define ursprunglig_fjärranslutning_huvud
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Förbereda_fjärr(void);
void 원격살피기(void);
void fjärr_utleverans(unsigned char);
int fjärr_indata(void);
int feed_fjärr_indata(const unsigned char *,unsigned);
uintptr_t Tavla_skuggning(uintptr_t,uintptr_t);
uintptr_t Tavla_avsluta_fjärr_kommando(uintptr_t);
uintptr_t Tavla_fjärr_vänta(uintptr_t);
void 원격화면살피기(void);
int kontroll_fjärr_visa(unsigned);
#endif
