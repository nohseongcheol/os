#ifndef natywny_użytkownik_Nagłówek
#define natywny_użytkownik_Nagłówek
#include <stdint.h>
#include <stddef.h>
#define użytkownik_baza 0x02000000ul
#define użytkownik_OBRAZ_Koniec 0x02c00000ul
#define użytkownik_sterta_Koniec 0x02ed0000ul
#define użytkownik_Stos_ADRES 0x02f00000ul
#define użytkownik_Koniec 0x03000000ul
#define użytkownik_strona_ILE_LICZB ((użytkownik_Koniec - użytkownik_baza) / 4096ul)
#define użytkownik_wykonywalny_błąd (-8)
#define użytkownik_dane_błąd (-1001)
#define użytkownik_wykonanie_błąd (-1002)
#define użytkownik_nieważny_instrukcja (-1003)
#define użytkownik_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t rejestr_dane[31], polecenie_stanowisko, Stan_KOD, Stos_ADRES; } użytkownik_kadr;
void 사용자체계준비(void);
int wyjątek_użytkownika(użytkownik_kadr *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Tablica_użytkownik_przebieg(uintptr_t);
uintptr_t Tablica_użytkownik_walidować(void);
uintptr_t Tablica_formant_użytkownika(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
