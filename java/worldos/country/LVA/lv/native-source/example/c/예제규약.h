#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int 글길이(const char *Teksts) { int 길이=0;while(Teksts[길이])길이++;return 길이; }
static int Izvade(const char *Teksts) { int 길이=글길이(Teksts);return rakstīšana_Fails_dati(1,Teksts,길이)==길이?0:1; }
#endif
