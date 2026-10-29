#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int 글길이(const char *Besedilo) { int 길이=0;while(Besedilo[길이])길이++;return 길이; }
static int Izpis(const char *Besedilo) { int 길이=글길이(Besedilo);return pisati_Datoteka_podatki(1,Besedilo,길이)==길이?0:1; }
#endif
