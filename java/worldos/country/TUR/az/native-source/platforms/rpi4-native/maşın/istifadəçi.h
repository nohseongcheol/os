#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define istifadəçi_BASE 0x02000000ul
#define istifadəçi_IMAGE_bitirmək 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define istifadəçi_Yığın_ünvan 0x02f00000ul
#define istifadəçi_bitirmək 0x03000000ul
#define istifadəçi_səhifə_COUNT ((istifadəçi_bitirmək - istifadəçi_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define istifadəçi_verilənlər_səhv (-1001)
#define 사용자실행오류 (-1002)
#define istifadəçi_yanlış_təlimat (-1003)
#define istifadəçi_FASİLƏ (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t qeydiyyatdan_keçmək_verilənlər[31], əmr_yerinə_qoymaq, vəziyyət_kod, Yığın_ünvan; } istifadəçi_kadr;
void 사용자체계준비(void);
int istifadəçi_istisna(istifadəçi_kadr *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t lövhə_istifadəçi_icra(uintptr_t);
uintptr_t lövhə_istifadəçi_təsdiqlə(void);
uintptr_t lövhə_istifadəçi_idarəetməsi(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
