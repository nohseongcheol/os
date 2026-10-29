#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_haba(const char *SMS) { int haba_VALUE=0;while(SMS[haba_VALUE])haba_VALUE++;return haba_VALUE; }
static int 출력(const char *SMS) { int haba_VALUE=SMS_haba(SMS);return sumulat_file_data(1,SMS,haba_VALUE)==haba_VALUE?0:1; }
#endif
