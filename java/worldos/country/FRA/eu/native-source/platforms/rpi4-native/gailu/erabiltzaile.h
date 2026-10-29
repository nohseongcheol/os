#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define erabiltzaile_BASE 0x02000000ul
#define erabiltzaile_irudi_amaitu 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define erabiltzaile_pila_helbide 0x02f00000ul
#define erabiltzaile_amaitu 0x03000000ul
#define erabiltzaile_orri_ZENBATU ((erabiltzaile_amaitu - erabiltzaile_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define erabiltzaile_datuak_errore (-1001)
#define 사용자실행오류 (-1002)
#define erabiltzaile_baliogabe_instrukzio (-1003)
#define erabiltzaile_DENBORA_MUGA (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t izena_eman_datuak[31], komando_kargu, Egoera_KODE, pila_helbide; } erabiltzaile_marko;
void 사용자체계준비(void);
int erabiltzaile_salbuespen(erabiltzaile_marko *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t arbel_erabiltzaile_exekutatu(uintptr_t);
uintptr_t arbel_erabiltzaile_baliozkotu(void);
uintptr_t arbel_erabiltzaile_kontrola(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
