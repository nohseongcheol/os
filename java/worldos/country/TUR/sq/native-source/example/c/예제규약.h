#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_gjatësi(const char *Teksti) { int gjatësi_VALUE=0;while(Teksti[gjatësi_VALUE])gjatësi_VALUE++;return gjatësi_VALUE; }
static int 출력(const char *Teksti) { int gjatësi_VALUE=SMS_gjatësi(Teksti);return shkruaj_skedar_të_dhëna(1,Teksti,gjatësi_VALUE)==gjatësi_VALUE?0:1; }
#endif
