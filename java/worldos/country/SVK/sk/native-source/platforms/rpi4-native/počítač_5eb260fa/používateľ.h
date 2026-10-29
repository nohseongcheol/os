#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define používateľ_BASE 0x02000000ul
#define používateľ_IMAGE_ukončiť_hovor 0x02c00000ul
#define používateľ_halda_ukončiť_hovor 0x02ed0000ul
#define používateľ_Vrstvy_adresa 0x02f00000ul
#define používateľ_ukončiť_hovor 0x03000000ul
#define používateľ_strana_COUNT ((používateľ_ukončiť_hovor - používateľ_BASE) / 4096ul)
#define používateľ_spustiteľný_súbor_Chyba (-8)
#define používateľ_údaje_Chyba (-1001)
#define 사용자실행오류 (-1002)
#define používateľ_neplatné_inštrukcia (-1003)
#define používateľ_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t register_údaje[31], príkaz_pozícia, Stav_kód, Vrstvy_adresa; } používateľ_rám;
void 사용자체계준비(void);
int používateľská_výnimka(používateľ_rám *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Panel_používateľ_spustiť(uintptr_t);
uintptr_t Panel_používateľ_overiť(void);
uintptr_t Panel_používateľský_ovládací_prvok(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
