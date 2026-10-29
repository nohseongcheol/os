#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_diir(const char *Tekst) { int diir_xëyma=0;while(Tekst[diir_xëyma])diir_xëyma++;return diir_xëyma; }
static int 출력(const char *Tekst) { int diir_xëyma=SMS_diir(Tekst);return biir_bara_denc_mbir(1,Tekst,diir_xëyma)==diir_xëyma?0:1; }
#endif
