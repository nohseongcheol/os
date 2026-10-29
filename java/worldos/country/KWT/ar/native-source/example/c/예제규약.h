#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int طول_النص_بالبايت(const char *نص) { int 길이=0;while(نص[길이])길이++;return 길이; }
static int مخرجات(const char *نص) { int 길이=طول_النص_بالبايت(نص);return كتابة_ملف_بيانات(1,نص,길이)==길이?0:1; }
#endif
