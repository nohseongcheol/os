#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int I_SMS_ubude(const char *Umbhalo) { int ubude_ixabiso=0;while(Umbhalo[ubude_ixabiso])ubude_ixabiso++;return ubude_ixabiso; }
static int 출력(const char *Umbhalo) { int ubude_ixabiso=I_SMS_ubude(Umbhalo);return bhala_ifayile_iingcombolo(1,Umbhalo,ubude_ixabiso)==ubude_ixabiso?0:1; }
#endif
