#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int tekstin_pituus_tavuina(const char *teksti) { int kesto_ARVO=0;while(teksti[kesto_ARVO])kesto_ARVO++;return kesto_ARVO; }
static int tulostuspaikka(const char *teksti) { int kesto_ARVO=tekstin_pituus_tavuina(teksti);return kirjoitus_Tiedosto_data(1,teksti,kesto_ARVO)==kesto_ARVO?0:1; }
#endif
