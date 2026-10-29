#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define brukar_BASE 0x02000000ul
#define brukar_IMAGE_avslutte 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define brukar_Stabel_ADDRESS 0x02f00000ul
#define brukar_avslutte 0x03000000ul
#define brukar_side_COUNT ((brukar_avslutte - brukar_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define brukar_data_feil (-1001)
#define 사용자실행오류 (-1002)
#define brukar_ugyldig_instruksjon (-1003)
#define brukar_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t registrere_data[31], kommando_plassere, status_CODE, Stabel_ADDRESS; } brukar_rute;
void 사용자체계준비(void);
int brukar_unntak(brukar_rute *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Tavle_brukar_køyre(uintptr_t);
uintptr_t Tavle_brukar_bekrefte(void);
uintptr_t Tavle_brukarkontroll(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
