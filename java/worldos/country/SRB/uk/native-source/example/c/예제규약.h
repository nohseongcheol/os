#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int довжина_тексту_в_байтах(const char *текст) { int 길이=0;while(текст[길이])길이++;return 길이; }
static int Вивід(const char *текст) { int 길이=довжина_тексту_в_байтах(текст);return записування_Файл_дані(1,текст,길이)==길이?0:1; }
#endif
