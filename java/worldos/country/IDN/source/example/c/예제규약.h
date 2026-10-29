#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int panjang_teks_dalam_byte(const char *teks) { int panjang_VALUE=0;while(teks[panjang_VALUE])panjang_VALUE++;return panjang_VALUE; }
static int keluaranTeks(const char *teks) { int panjang_VALUE=panjang_teks_dalam_byte(teks);return tulis_file_data(1,teks,panjang_VALUE)==panjang_VALUE?0:1; }
#endif
