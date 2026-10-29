#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int СМС_озынлык(const char *Mäten) { int озынлык_VALUE=0;while(Mäten[озынлык_VALUE])озынлык_VALUE++;return озынлык_VALUE; }
static int 출력(const char *Mäten) { int озынлык_VALUE=СМС_озынлык(Mäten);return язу_файл_мәгълүмат(1,Mäten,озынлык_VALUE)==озынлык_VALUE?0:1; }
#endif
