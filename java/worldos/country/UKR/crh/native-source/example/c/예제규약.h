#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int 글길이(const char *Metin) { int 길이=0;while(Metin[길이])길이++;return 길이; }
static int 출력(const char *Metin) { int 길이=글길이(Metin);return 파일자료쓰기(1,Metin,길이)==길이?0:1; }
#endif
