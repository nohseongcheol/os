#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int textlängd_i_byte(const char *text) { int längd_värde=0;while(text[längd_värde])längd_värde++;return längd_värde; }
static int utmatningsposition(const char *text) { int längd_värde=textlängd_i_byte(text);return skriva_fil_data(1,text,längd_värde)==längd_värde?0:1; }
#endif
