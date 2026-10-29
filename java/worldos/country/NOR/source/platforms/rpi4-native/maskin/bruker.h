#ifndef opprinnelig_bruker_Topptekst
#define opprinnelig_bruker_Topptekst
#include <stdint.h>
#include <stddef.h>
#define bruker_grunnlag 0x02000000ul
#define bruker_BILDE_avslutte_en_samtale 0x02c00000ul
#define bruker_heap_avslutte_en_samtale 0x02ed0000ul
#define bruker_stakk_e_post 0x02f00000ul
#define bruker_avslutte_en_samtale 0x03000000ul
#define bruker_page_ANTALL ((bruker_avslutte_en_samtale - bruker_grunnlag) / 4096ul)
#define bruker_kjørbar_fil_feil (-8)
#define bruker_data_feil (-1001)
#define bruker_kjøring_feil (-1002)
#define 사용자잘못된명령 (-1003)
#define bruker_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t register_data[31], kommando_plassere, status_KODE, stakk_e_post; } bruker_bilde;
void 사용자체계준비(void);
int bruker_unntak(bruker_bilde *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Tavle_bruker_kjøre(uintptr_t);
uintptr_t Tavle_bruker_bekrefte(void);
uintptr_t Tavle_brukerkontroll(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
