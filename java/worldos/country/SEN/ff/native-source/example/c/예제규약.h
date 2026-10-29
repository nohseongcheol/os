#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int binndi_njuuteendi(const char *binndi) { int njuuteendi_njaru=0;while(binndi[njuuteendi_njaru])njuuteendi_njaru++;return njuuteendi_njaru; }
static int 출력(const char *binndi) { int njuuteendi_njaru=binndi_njuuteendi(binndi);return winndude_fiilde_keɓe(1,binndi,njuuteendi_njaru)==njuuteendi_njaru?0:1; }
#endif
