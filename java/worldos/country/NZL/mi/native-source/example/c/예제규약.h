#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int TEXT_roa(const char *Ngā_kupu) { int roa_uara=0;while(Ngā_kupu[roa_uara])roa_uara++;return roa_uara; }
static int 출력(const char *Ngā_kupu) { int roa_uara=TEXT_roa(Ngā_kupu);return tuhi_kōnae_raraunga(1,Ngā_kupu,roa_uara)==roa_uara?0:1; }
#endif
