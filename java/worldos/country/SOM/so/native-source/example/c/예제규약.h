#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int 글길이(const char *글) { int 길이=0;while(글[길이])길이++;return 길이; }
static int 출력(const char *글) { int 길이=글길이(글);return 파일자료쓰기(1,글,길이)==길이?0:1; }
#endif
