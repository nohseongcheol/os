#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_lengd(const char *Tekst) { int lengd_VALUE=0;while(Tekst[lengd_VALUE])lengd_VALUE++;return lengd_VALUE; }
static int Utdata(const char *Tekst) { int lengd_VALUE=SMS_lengd(Tekst);return skrive_fil_data(1,Tekst,lengd_VALUE)==lengd_VALUE?0:1; }
#endif
