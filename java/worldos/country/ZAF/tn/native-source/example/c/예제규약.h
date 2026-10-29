#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_boleele(const char *SMS) { int boleele_Boleng=0;while(SMS[boleele_Boleng])boleele_Boleng++;return boleele_Boleng; }
static int 출력(const char *SMS) { int boleele_Boleng=SMS_boleele(SMS);return kwala_faele_tshedimosetso(1,SMS,boleele_Boleng)==boleele_Boleng?0:1; }
#endif
