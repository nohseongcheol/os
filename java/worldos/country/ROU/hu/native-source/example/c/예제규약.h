#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_hossz(const char *Szöveg) { int hossz_ÉRTÉK=0;while(Szöveg[hossz_ÉRTÉK])hossz_ÉRTÉK++;return hossz_ÉRTÉK; }
static int Kimenet(const char *Szöveg) { int hossz_ÉRTÉK=SMS_hossz(Szöveg);return ír_Fájl_adat(1,Szöveg,hossz_ÉRTÉK)==hossz_ÉRTÉK?0:1; }
#endif
