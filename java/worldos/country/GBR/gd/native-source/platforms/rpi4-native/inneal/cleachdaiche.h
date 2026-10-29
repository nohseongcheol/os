#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define cleachdaiche_BASE 0x02000000ul
#define cleachdaiche_IMAGE_crìochnaich 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define cleachdaiche_stac_ADDRESS 0x02f00000ul
#define cleachdaiche_crìochnaich 0x03000000ul
#define cleachdaiche_duilleag_COUNT ((cleachdaiche_crìochnaich - cleachdaiche_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define cleachdaiche_dàta_mearachd (-1001)
#define 사용자실행오류 (-1002)
#define cleachdaiche_mì_dhligheach_treòrachadh (-1003)
#define cleachdaiche_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t clàraich_dàta[31], àithne_suidhich, cor_CODE, stac_ADDRESS; } cleachdaiche_frèam;
void 사용자체계준비(void);
int 사용자예외(cleachdaiche_frèam *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t bòrd_cleachdaiche_ruith(uintptr_t);
uintptr_t bòrd_cleachdaiche_dearbh(void);
uintptr_t bòrd_uidheam_smachd_cleachdaiche(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
