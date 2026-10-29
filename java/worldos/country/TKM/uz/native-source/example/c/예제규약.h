#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_uzunlik(const char *Matn) { int uzunlik_VALUE=0;while(Matn[uzunlik_VALUE])uzunlik_VALUE++;return uzunlik_VALUE; }
static int 출력(const char *Matn) { int uzunlik_VALUE=SMS_uzunlik(Matn);return yozmoq_fayl_ma_lumotlar(1,Matn,uzunlik_VALUE)==uzunlik_VALUE?0:1; }
#endif
