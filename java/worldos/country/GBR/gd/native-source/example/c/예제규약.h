#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_faid(const char *SMS) { int faid_VALUE=0;while(SMS[faid_VALUE])faid_VALUE++;return faid_VALUE; }
static int 출력(const char *SMS) { int faid_VALUE=SMS_faid(SMS);return sgrìobh_faidhle_dàta(1,SMS,faid_VALUE)==faid_VALUE?0:1; }
#endif
