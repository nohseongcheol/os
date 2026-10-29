#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int 글길이(const char *Tekst) { int 길이=0;while(Tekst[길이])길이++;return 길이; }
static int Izlaz(const char *Tekst) { int 길이=글길이(Tekst);return zapisivanje_Datoteka_podaci(1,Tekst,길이)==길이?0:1; }
#endif
