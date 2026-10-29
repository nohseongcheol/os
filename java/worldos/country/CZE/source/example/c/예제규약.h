#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <Soubor_ABI.h>
#include <화면규약.h>
static int délka_textu_v_bajtech(const char *text) { int délka_HODNOTA=0;while(text[délka_HODNOTA])délka_HODNOTA++;return délka_HODNOTA; }
static int výstupní_pozice(const char *text) { int délka_HODNOTA=délka_textu_v_bajtech(text);return zápis_Soubor_data(1,text,délka_HODNOTA)==délka_HODNOTA?0:1; }
#endif
