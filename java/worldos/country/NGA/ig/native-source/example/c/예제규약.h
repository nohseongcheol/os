#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_ogologo(const char *SMS) { int ogologo_valuu=0;while(SMS[ogologo_valuu])ogologo_valuu++;return ogologo_valuu; }
static int 출력(const char *SMS) { int ogologo_valuu=SMS_ogologo(SMS);return dee_ọbọakwụkwọ_datà(1,SMS,ogologo_valuu)==ogologo_valuu?0:1; }
#endif
