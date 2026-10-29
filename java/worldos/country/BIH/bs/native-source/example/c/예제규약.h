#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_dužina(const char *Tekst) { int dužina_VALUE=0;while(Tekst[dužina_VALUE])dužina_VALUE++;return dužina_VALUE; }
static int Ispis(const char *Tekst) { int dužina_VALUE=SMS_dužina(Tekst);return pisati_fajl_podaci(1,Tekst,dužina_VALUE)==dužina_VALUE?0:1; }
#endif
