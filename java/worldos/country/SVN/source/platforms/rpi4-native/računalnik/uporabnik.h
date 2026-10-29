#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define uporabnik_BASE 0x02000000ul
#define uporabnik_IMAGE_končati_klic 0x02c00000ul
#define uporabnik_kopica_končati_klic 0x02ed0000ul
#define uporabnik_Sklad_naslov 0x02f00000ul
#define uporabnik_končati_klic 0x03000000ul
#define uporabnik_stran_COUNT ((uporabnik_končati_klic - uporabnik_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define 사용자자료오류 (-1001)
#define 사용자실행오류 (-1002)
#define uporabnik_neveljaven_navodilo (-1003)
#define uporabnik_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t register_podatki[31], ukaz_položaj, stanje_CODE, Sklad_naslov; } uporabnik_okvir;
void 사용자체계준비(void);
int izjema_uporabniškega_načina(uporabnik_okvir *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Tabla_uporabnik_izvajati(uintptr_t);
uintptr_t Tabla_uporabnik_preveriti_veljavnost(void);
uintptr_t Tabla_uporabniški_kontrolnik(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
