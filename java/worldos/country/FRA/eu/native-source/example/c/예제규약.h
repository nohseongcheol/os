#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_luzera(const char *Testua) { int luzera_balio=0;while(Testua[luzera_balio])luzera_balio++;return luzera_balio; }
static int Irteera(const char *Testua) { int luzera_balio=SMS_luzera(Testua);return idatzi_fitxategi_datuak(1,Testua,luzera_balio)==luzera_balio?0:1; }
#endif
