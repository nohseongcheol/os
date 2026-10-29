#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_lengde(const char *Tekst) { int lengde_VERDI=0;while(Tekst[lengde_VERDI])lengde_VERDI++;return lengde_VERDI; }
static int Utgang(const char *Tekst) { int lengde_VERDI=SMS_lengde(Tekst);return skrive_Fil_data(1,Tekst,lengde_VERDI)==lengde_VERDI?0:1; }
#endif
