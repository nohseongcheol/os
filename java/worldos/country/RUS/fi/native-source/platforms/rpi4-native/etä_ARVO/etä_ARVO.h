#ifndef alkuperäinen_etäyhteys_otsikko
#define alkuperäinen_etäyhteys_otsikko
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Valmistele_etä(void);
void 원격살피기(void);
void etä_tulos(unsigned char);
int etä_syöte(void);
int syöte_etä_syöte(const unsigned char *,unsigned);
uintptr_t Taulu_etähallinta(uintptr_t,uintptr_t);
uintptr_t Taulu_lopettaa_puhelu_etä_komento(uintptr_t);
uintptr_t Taulu_etä_odottaa(uintptr_t);
void 원격화면살피기(void);
int ohjain_etä_näyttö(unsigned);
#endif
