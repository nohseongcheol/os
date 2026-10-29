#ifndef natywny_połączenie_zdalne_Nagłówek
#define natywny_połączenie_zdalne_Nagłówek
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Przygotuj_zdalny(void);
void 원격살피기(void);
void zdalny_produkt_wyjściowy(unsigned char);
int zdalny_wejście(void);
int kanał_zdalny_wejście(const unsigned char *,unsigned);
uintptr_t Tablica_obserwowanie(uintptr_t,uintptr_t);
uintptr_t Tablica_Koniec_zdalny_polecenie(uintptr_t);
uintptr_t Tablica_zdalny_chwileczkę(uintptr_t);
void 원격화면살피기(void);
int kontrola_zdalny_wyświetlać(unsigned);
#endif
