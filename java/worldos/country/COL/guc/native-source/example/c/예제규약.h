#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int 글길이(const char *글) { int akaliaa_ajutuu=0;while(글[akaliaa_ajutuu])akaliaa_ajutuu++;return akaliaa_ajutuu; }
static int 출력(const char *글) { int akaliaa_ajutuu=글길이(글);return ashajaa_anaajaalaa_atijaaya(1,글,akaliaa_ajutuu)==akaliaa_ajutuu?0:1; }
#endif
