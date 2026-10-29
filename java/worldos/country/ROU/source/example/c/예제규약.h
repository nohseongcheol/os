#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_lungime(const char *SMS) { int lungime_VALUE=0;while(SMS[lungime_VALUE])lungime_VALUE++;return lungime_VALUE; }
static int Rezultat(const char *SMS) { int lungime_VALUE=SMS_lungime(SMS);return scriere_Fișier_date(1,SMS,lungime_VALUE)==lungime_VALUE?0:1; }
#endif
