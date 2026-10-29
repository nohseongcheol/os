#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_uzunluq(const char *Mətn) { int uzunluq_VALUE=0;while(Mətn[uzunluq_VALUE])uzunluq_VALUE++;return uzunluq_VALUE; }
static int 출력(const char *Mətn) { int uzunluq_VALUE=SMS_uzunluq(Mətn);return yazmaq_fayl_verilənlər(1,Mətn,uzunluq_VALUE)==uzunluq_VALUE?0:1; }
#endif
