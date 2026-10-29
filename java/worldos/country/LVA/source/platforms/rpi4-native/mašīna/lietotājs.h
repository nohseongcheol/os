#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define lietotājs_BASE 0x02000000ul
#define lietotājs_IMAGE_beigt_zvanu 0x02c00000ul
#define lietotājs_kaudze_beigt_zvanu 0x02ed0000ul
#define lietotājs_kopa_adrese 0x02f00000ul
#define lietotājs_beigt_zvanu 0x03000000ul
#define lietotājs_lapa_COUNT ((lietotājs_beigt_zvanu - lietotājs_BASE) / 4096ul)
#define lietotājs_izpildāms_fails_kļūda (-8)
#define lietotājs_dati_kļūda (-1001)
#define 사용자실행오류 (-1002)
#define 사용자잘못된명령 (-1003)
#define lietotājs_NOILGUMS (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t reģistrs_dati[31], komanda_amats, Statuss_CODE, kopa_adrese_0062a350; } lietotājs_kadrs;
void 사용자체계준비(void);
int lietotāja_izņēmums(lietotājs_kadrs *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Panelis_lietotājs_virkne(uintptr_t);
uintptr_t Panelis_lietotājs_validēt(void);
uintptr_t Panelis_lietotāja_vadīkla(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
