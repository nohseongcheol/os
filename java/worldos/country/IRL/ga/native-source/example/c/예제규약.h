#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_fad(const char *Téacs) { int fad_VALUE=0;while(Téacs[fad_VALUE])fad_VALUE++;return fad_VALUE; }
static int Aschur(const char *Téacs) { int fad_VALUE=SMS_fad(Téacs);return scríobh_comhad_sonraí(1,Téacs,fad_VALUE)==fad_VALUE?0:1; }
#endif
