#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_uburebure(const char *Umwandiko) { int uburebure_agaciro=0;while(Umwandiko[uburebure_agaciro])uburebure_agaciro++;return uburebure_agaciro; }
static int 출력(const char *Umwandiko) { int uburebure_agaciro=SMS_uburebure(Umwandiko);return kwandika_dosiye_amakurushingiro(1,Umwandiko,uburebure_agaciro)==uburebure_agaciro?0:1; }
#endif
