#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int પાઠ_લંબાઈ(const char *લખાણ) { int લંબાઈ_મૂલ્ય=0;while(લખાણ[લંબાઈ_મૂલ્ય])લંબાઈ_મૂલ્ય++;return લંબાઈ_મૂલ્ય; }
static int આઉટપુટ(const char *લખાણ) { int લંબાઈ_મૂલ્ય=પાઠ_લંબાઈ(લખાણ);return લખો_ફાઇલ_ડેટા(1,લખાણ,લંબાઈ_મૂલ્ય)==લંબાઈ_મૂલ્ય?0:1; }
#endif
