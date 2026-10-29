#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int 글길이(const char *Tekstas) { int 길이=0;while(Tekstas[길이])길이++;return 길이; }
static int Išvestis(const char *Tekstas) { int 길이=글길이(Tekstas);return rašymas_Failas_duomenys(1,Tekstas,길이)==길이?0:1; }
#endif
