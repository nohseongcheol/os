#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <Dosya_ABI.h>
#include <화면규약.h>
static int metnin_bayt_uzunluğu(const char *metin) { int süre_değer=0;while(metin[süre_değer])süre_değer++;return süre_değer; }
static int metinÇıktısı(const char *metin) { int süre_değer=metnin_bayt_uzunluğu(metin);return yazma_Dosya_veri(1,metin,süre_değer)==süre_değer?0:1; }
#endif
