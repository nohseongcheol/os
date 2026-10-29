#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int I_SMS_ubude(const char *Itekisi) { int ubude_inani=0;while(Itekisi[ubude_inani])ubude_inani++;return ubude_inani; }
static int 출력(const char *Itekisi) { int ubude_inani=I_SMS_ubude(Itekisi);return bhala_ifayela_imininingwane(1,Itekisi,ubude_inani)==ubude_inani?0:1; }
#endif
