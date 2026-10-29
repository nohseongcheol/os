#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int SMS_gígùn(const char *SMS) { int gígùn_iye=0;while(SMS[gígùn_iye])gígùn_iye++;return gígùn_iye; }
static int 출력(const char *SMS) { int gígùn_iye=SMS_gígùn(SMS);return kọ_fáìlì_détà(1,SMS,gígùn_iye)==gígùn_iye?0:1; }
#endif
