#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int СМС_должина(const char *Текст) { int должина_VALUE=0;while(Текст[должина_VALUE])должина_VALUE++;return должина_VALUE; }
static int 출력(const char *Текст) { int должина_VALUE=СМС_должина(Текст);return запиши_датотека_податоци(1,Текст,должина_VALUE)==должина_VALUE?0:1; }
#endif
