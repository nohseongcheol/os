#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_lengd(const char *Texti) { int lengd_VALUE=0;while(Texti[lengd_VALUE])lengd_VALUE++;return lengd_VALUE; }
static int úttak(const char *Texti) { int lengd_VALUE=SMS_lengd(Texti);return skrifa_skrá_gögn(1,Texti,lengd_VALUE)==lengd_VALUE?0:1; }
#endif
