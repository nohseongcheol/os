#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define kaiwhakamahi_BASE 0x02000000ul
#define kaiwhakamahi_IMAGE_mutu 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define kaiwhakamahi_Huinga_ADDRESS 0x02f00000ul
#define kaiwhakamahi_mutu 0x03000000ul
#define kaiwhakamahi_whārangi_COUNT ((kaiwhakamahi_mutu - kaiwhakamahi_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define kaiwhakamahi_raraunga_hapa (-1001)
#define 사용자실행오류 (-1002)
#define kaiwhakamahi_muhu_tohutohu (-1003)
#define kaiwhakamahi_KUA_PAU_TE_WĀ (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t rēhita_raraunga[31], tono_tūranga, tūnga_CODE, Huinga_ADDRESS; } kaiwhakamahi_tāpare;
void 사용자체계준비(void);
int 사용자예외(kaiwhakamahi_tāpare *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t papa_kaiwhakamahi_whakahaere(uintptr_t);
uintptr_t papa_kaiwhakamahi_whakamana(void);
uintptr_t papa_mana_kaiwhakamahi(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
