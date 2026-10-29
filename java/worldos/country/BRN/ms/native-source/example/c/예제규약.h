#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int panjang_teks_dalam_bait(const char *Teks) { int kepanjangan_VALUE=0;while(Teks[kepanjangan_VALUE])kepanjangan_VALUE++;return kepanjangan_VALUE; }
static int 출력(const char *Teks) { int kepanjangan_VALUE=panjang_teks_dalam_bait(Teks);return tulis_fail_data(1,Teks,kepanjangan_VALUE)==kepanjangan_VALUE?0:1; }
#endif
