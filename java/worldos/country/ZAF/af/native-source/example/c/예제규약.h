#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_lengte(const char *Teks) { int lengte_VALUE=0;while(Teks[lengte_VALUE])lengte_VALUE++;return lengte_VALUE; }
static int Afvoer(const char *Teks) { int lengte_VALUE=SMS_lengte(Teks);return skryf_lêer_data(1,Teks,lengte_VALUE)==lengte_VALUE?0:1; }
#endif
