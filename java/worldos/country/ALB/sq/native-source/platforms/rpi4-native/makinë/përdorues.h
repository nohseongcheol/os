#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define përdorues_BASE 0x02000000ul
#define përdorues_IMAGE_mbaroj 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define përdorues_Stivë_email 0x02f00000ul
#define përdorues_mbaroj 0x03000000ul
#define përdorues_faqe_COUNT ((përdorues_mbaroj - përdorues_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define përdorues_të_dhëna_gabim (-1001)
#define 사용자실행오류 (-1002)
#define përdorues_i_pavlefshëm_instruksion (-1003)
#define përdorues_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t regjistroj_të_dhëna[31], komandë_pozicioni, status_kod, Stivë_email; } përdorues_kuadër;
void 사용자체계준비(void);
int përdorues_përjashtim(përdorues_kuadër *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t panel_përdorues_varg(uintptr_t);
uintptr_t panel_përdorues_vlerësoj(void);
uintptr_t panel_kontroll_përdoruesi(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
