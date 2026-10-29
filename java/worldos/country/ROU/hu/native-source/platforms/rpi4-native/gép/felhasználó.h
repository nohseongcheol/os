#ifndef natív_felhasználó_fejléc
#define natív_felhasználó_fejléc
#include <stdint.h>
#include <stddef.h>
#define felhasználó_ALAP 0x02000000ul
#define felhasználó_KÉP_megszüntet 0x02c00000ul
#define felhasználó_halommemória_megszüntet 0x02ed0000ul
#define felhasználó_Sor_CÍM 0x02f00000ul
#define felhasználó_megszüntet 0x03000000ul
#define felhasználó_lap_DARAB ((felhasználó_megszüntet - felhasználó_ALAP) / 4096ul)
#define felhasználó_végrehajtható_hiba (-8)
#define felhasználó_adat_hiba (-1001)
#define felhasználó_végrehajtás_hiba (-1002)
#define 사용자잘못된명령 (-1003)
#define felhasználó_IDŐTÚLLÉPÉS (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t jegyzék_adat[31], parancs_pozíció, Állapot_KÓD, Sor_CÍM; } felhasználó_doboz;
void 사용자체계준비(void);
int alkalmazáskivétel(felhasználó_doboz *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t fal_felhasználó_futtat(uintptr_t);
uintptr_t fal_felhasználó_ellenőriz(void);
uintptr_t fal_egyéni_vezérlőelem(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
