#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_botelele(const char *Sengwalwa) { int botelele_boleng=0;while(Sengwalwa[botelele_boleng])botelele_boleng++;return botelele_boleng; }
static int 출력(const char *Sengwalwa) { int botelele_boleng=SMS_botelele(Sengwalwa);return ngwala_faele_data(1,Sengwalwa,botelele_boleng)==botelele_boleng?0:1; }
#endif
