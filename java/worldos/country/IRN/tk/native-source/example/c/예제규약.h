#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_dowamlylyk(const char *Metin) { int dowamlylyk_baha=0;while(Metin[dowamlylyk_baha])dowamlylyk_baha++;return dowamlylyk_baha; }
static int 출력(const char *Metin) { int dowamlylyk_baha=SMS_dowamlylyk(Metin);return ýaz_faýl_maglumat(1,Metin,dowamlylyk_baha)==dowamlylyk_baha?0:1; }
#endif
