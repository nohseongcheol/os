#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_Tsawo(const char *SMS) { int Tsawo_Daraja=0;while(SMS[Tsawo_Daraja])Tsawo_Daraja++;return Tsawo_Daraja; }
static int 출력(const char *SMS) { int Tsawo_Daraja=SMS_Tsawo(SMS);return Rubuta_Fayil_Tarin_bayani(1,SMS,Tsawo_Daraja)==Tsawo_Daraja?0:1; }
#endif
