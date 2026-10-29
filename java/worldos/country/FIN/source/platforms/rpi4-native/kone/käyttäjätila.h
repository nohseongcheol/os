#ifndef alkuperäinen_käyttäjä_otsikko
#define alkuperäinen_käyttäjä_otsikko
#include <stdint.h>
#include <stddef.h>
#define käyttäjä_PERUS 0x02000000ul
#define käyttäjä_KUVA_lopettaa_puhelu 0x02c00000ul
#define käyttäjä_keko_lopettaa_puhelu 0x02ed0000ul
#define käyttäjä_Pino_OSOITE 0x02f00000ul
#define käyttäjä_lopettaa_puhelu 0x03000000ul
#define käyttäjä_page_LASKE ((käyttäjä_lopettaa_puhelu - käyttäjä_PERUS) / 4096ul)
#define käyttäjä_suoritettava_tiedosto_virhe (-8)
#define käyttäjä_data_virhe (-1001)
#define käyttäjä_suoritus_virhe (-1002)
#define käyttäjä_pätemätön_käsky (-1003)
#define käyttäjä_AIKAKATKAISU (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t rekisteri_data[31], komento_toimi, Tila_KOODI, Pino_OSOITE; } käyttäjä_kuva;
void 사용자체계준비(void);
int käyttäjäpoikkeus(käyttäjä_kuva *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Taulu_käyttäjä_suorittaa(uintptr_t);
uintptr_t Taulu_käyttäjä_vahvista(void);
uintptr_t Taulu_käyttäjän_ohjausobjekti(uintptr_t);
uint32_t lukea_käyttäjä_Tila(unsigned, unsigned);
#endif
