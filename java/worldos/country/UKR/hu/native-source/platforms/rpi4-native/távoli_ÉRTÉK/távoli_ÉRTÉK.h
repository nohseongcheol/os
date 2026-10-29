#ifndef natív_távoli_kapcsolat_fejléc
#define natív_távoli_kapcsolat_fejléc
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Előkészítés_távoli(void);
void 원격살피기(void);
void távoli_kimenet(unsigned char);
int távoli_bevitel(void);
int csatorna_távoli_bevitel(const unsigned char *,unsigned);
uintptr_t fal_távkezelés(uintptr_t,uintptr_t);
uintptr_t fal_megszüntet_távoli_parancs(uintptr_t);
uintptr_t fal_távoli_várj(uintptr_t);
void 원격화면살피기(void);
int vezérlő_távoli_kijelző(unsigned);
#endif
