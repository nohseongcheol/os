#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <Plik_ABI.h>
#include <화면규약.h>
static int długość_tekstu_w_bajtach(const char *tekst) { int długość_WARTOŚĆ=0;while(tekst[długość_WARTOŚĆ])długość_WARTOŚĆ++;return długość_WARTOŚĆ; }
static int pozycja_wyjścia(const char *tekst) { int długość_WARTOŚĆ=długość_tekstu_w_bajtach(tekst);return zapis_Plik_dane(1,tekst,długość_WARTOŚĆ)==długość_WARTOŚĆ?0:1; }
#endif
