#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define korisnik_BASE 0x02000000ul
#define korisnik_IMAGE_završiti 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define korisnik_snop_adresa 0x02f00000ul
#define korisnik_završiti 0x03000000ul
#define korisnik_stranica_COUNT ((korisnik_završiti - korisnik_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define korisnik_podaci_greška (-1001)
#define 사용자실행오류 (-1002)
#define korisnik_nevažeće_programska_naredba (-1003)
#define korisnik_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t registrirati_podaci[31], komanda_položaj, stanje_kod, snop_adresa; } korisnik_kadar;
void 사용자체계준비(void);
int korisnik_izuzetak(korisnik_kadar *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t ploča_korisnik_niz(uintptr_t);
uintptr_t ploča_korisnik_ovjeriti(void);
uintptr_t ploča_korisnička_kontrola(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
