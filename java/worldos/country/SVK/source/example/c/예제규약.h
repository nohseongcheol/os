#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_dĺžka(const char *Spracovanie_textu) { int dĺžka_VALUE=0;while(Spracovanie_textu[dĺžka_VALUE])dĺžka_VALUE++;return dĺžka_VALUE; }
static int Výstup(const char *Spracovanie_textu) { int dĺžka_VALUE=SMS_dĺžka(Spracovanie_textu);return zapísať_Súbor_údaje(1,Spracovanie_textu,dĺžka_VALUE)==dĺžka_VALUE?0:1; }
#endif
