#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int 글길이(const char *Testu) { int 길이=0;while(Testu[길이])길이++;return 길이; }
static int Salida(const char *Testu) { int 길이=글길이(Testu);return 파일자료쓰기(1,Testu,길이)==길이?0:1; }
#endif
