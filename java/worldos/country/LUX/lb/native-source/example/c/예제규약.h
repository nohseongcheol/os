#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_Längt(const char *SMS) { int Längt_VALUE=0;while(SMS[Längt_VALUE])Längt_VALUE++;return Längt_VALUE; }
static int 출력(const char *SMS) { int Längt_VALUE=SMS_Längt(SMS);return schreiwen_Fichier_Daten(1,SMS,Längt_VALUE)==Längt_VALUE?0:1; }
#endif
