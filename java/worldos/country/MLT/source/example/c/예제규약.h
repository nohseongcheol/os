#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_tul(const char *SMS) { int tul_VALUE=0;while(SMS[tul_VALUE])tul_VALUE++;return tul_VALUE; }
static int 출력(const char *SMS) { int tul_VALUE=SMS_tul(SMS);return kiteb_fajl_data(1,SMS,tul_VALUE)==tul_VALUE?0:1; }
#endif
