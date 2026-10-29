#ifndef systeemeigen_externe_verbinding_header
#define systeemeigen_externe_verbinding_header
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Bereid_voor_extern(void);
void 원격살피기(void);
void extern_uitvoer(unsigned char);
int extern_invoer(void);
int feed_extern_invoer(const unsigned char *,unsigned);
uintptr_t Bord_extern_beheer(uintptr_t,uintptr_t);
uintptr_t Bord_beëindigen_extern_opdracht(uintptr_t);
uintptr_t Bord_extern_wachten(uintptr_t);
void 원격화면살피기(void);
int controle_extern_weergeven(unsigned);
#endif
