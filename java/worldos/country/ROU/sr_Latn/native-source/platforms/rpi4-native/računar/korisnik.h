#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define korisnik_BASE 0x02000000ul
#define korisnik_IMAGE_završiti_razgovor 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define korisnik_stek_adresa 0x02f00000ul
#define korisnik_završiti_razgovor 0x03000000ul
#define korisnik_stranica_COUNT ((korisnik_završiti_razgovor - korisnik_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define korisnik_podaci_greška (-1001)
#define 사용자실행오류 (-1002)
#define 사용자잘못된명령 (-1003)
#define korisnik_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t registar_podaci[31], komanda_pozicija, Status_kôd, stek_adresa; } korisnik_kadar;
void 사용자체계준비(void);
int greška_u_korisničkom_režimu(korisnik_kadar *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Tabla_korisnik_koristiti(uintptr_t);
uintptr_t Tabla_korisnik_potvrditi(void);
uintptr_t Tabla_korisnička_kontrola(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
