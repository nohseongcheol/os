#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_hyd(const char *Testun) { int hyd_VALUE=0;while(Testun[hyd_VALUE])hyd_VALUE++;return hyd_VALUE; }
static int Allbwn(const char *Testun) { int hyd_VALUE=SMS_hyd(Testun);return ysgrifennu_ffeil_data(1,Testun,hyd_VALUE)==hyd_VALUE?0:1; }
#endif
