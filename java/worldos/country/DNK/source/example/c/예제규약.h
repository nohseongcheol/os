#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int sms_varighed(const char *Tekst) { int varighed_VÆRDI=0;while(Tekst[varighed_VÆRDI])varighed_VÆRDI++;return varighed_VÆRDI; }
static int Udgang(const char *Tekst) { int varighed_VÆRDI=sms_varighed(Tekst);return skrive_fil_data(1,Tekst,varighed_VÆRDI)==varighed_VÆRDI?0:1; }
#endif
