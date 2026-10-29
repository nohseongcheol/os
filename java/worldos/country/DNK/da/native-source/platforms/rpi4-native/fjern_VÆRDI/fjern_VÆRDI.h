#ifndef oprindelig_fjernforbindelse_Header
#define oprindelig_fjernforbindelse_Header
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Tilrettelæg_fjern(void);
void 원격살피기(void);
void fjern_produktoutput(unsigned char);
int fjern_input(void);
int feed_fjern_input(const unsigned char *,unsigned);
uintptr_t Tavle_skygning(uintptr_t,uintptr_t);
uintptr_t Tavle_afslutte_et_opkald_fjern_kommando(uintptr_t);
uintptr_t Tavle_fjern_vent(uintptr_t);
void 원격화면살피기(void);
int kontrol_fjern_vise(unsigned);
#endif
